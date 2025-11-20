"""
Worker para procesar jobs
"""
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.job import Job, JobStatus, JobResult, JobSource
from app.services.perplexity import PerplexityService
from app.services.crawler import CrawlerService
from app.services.extractor import ExtractorService


def process_job(job_id: int):
    """
    Procesar un job completo:
    1. Descubrir URLs con Perplexity
    2. Crawlear URLs con Crawl4AI
    3. Extraer datos con LLM
    4. Guardar resultados
    """
    db: Session = SessionLocal()
    
    try:
        # Obtener job
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            print(f"Job {job_id} no encontrado")
            return
        
        # Actualizar status
        job.status = JobStatus.RUNNING
        db.commit()
        
        # 1. Descubrir URLs
        print(f"Descubriendo URLs para job {job_id}...")
        perplexity = PerplexityService()
        urls = []
        try:
            import asyncio
            urls = asyncio.run(perplexity.discover_urls(job.prompt, max_urls=20))
        except Exception as e:
            print(f"Error descubriendo URLs: {e}")
            job.status = JobStatus.FAILED
            job.error_message = f"Error descubriendo URLs: {str(e)}"
            db.commit()
            return
        
        # Guardar sources
        for url in urls:
            source = JobSource(job_id=job_id, url=url, status="pending")
            db.add(source)
        db.commit()
        
        # 2. Crawlear URLs
        print(f"Crawleando {len(urls)} URLs...")
        crawler = CrawlerService()
        contents = []
        
        for source in db.query(JobSource).filter(JobSource.job_id == job_id).all():
            try:
                import asyncio
                content = asyncio.run(crawler.crawl_url(source.url))
                if content:
                    contents.append((source.url, content))
                    source.status = "crawled"
                else:
                    source.status = "failed"
            except Exception as e:
                print(f"Error crawleando {source.url}: {e}")
                source.status = "failed"
            db.commit()
        
        # 3. Extraer datos
        print(f"Extrayendo datos de {len(contents)} páginas...")
        extractor = ExtractorService()
        all_results = []
        
        # Determinar límite según plan del usuario
        max_items = 200 if job.owner.plan == "free" else 2000
        
        for url, content in contents:
            try:
                import asyncio
                items = asyncio.run(
                    extractor.extract_structured_data(
                        job.prompt,
                        content,
                        max_items=max_items
                    )
                )
                
                for item in items:
                    result = JobResult(
                        job_id=job_id,
                        data=item,
                        source_url=url
                    )
                    db.add(result)
                    all_results.append(item)
                    
                    if len(all_results) >= max_items:
                        break
                        
            except Exception as e:
                print(f"Error extrayendo datos de {url}: {e}")
            
            if len(all_results) >= max_items:
                break
        
        db.commit()
        
        # Actualizar job
        job.status = JobStatus.COMPLETED
        job.total_items = len(all_results)
        job.items_processed = len(all_results)
        job.completed_at = datetime.utcnow()
        db.commit()
        
        print(f"Job {job_id} completado con {len(all_results)} items")
        
    except Exception as e:
        print(f"Error procesando job {job_id}: {e}")
        job = db.query(Job).filter(Job.id == job_id).first()
        if job:
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            db.commit()
    finally:
        db.close()

