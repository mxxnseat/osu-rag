from app.services.faq import FaqServiceDep, FaqService


def faq_service(service: FaqServiceDep) -> FaqService:
    return service