"""
Payments API - Placeholder for Mercado Pago integration (FASE 2).

This module provides the endpoint structure for future payment processing.
Currently returns informational responses only.
"""

from fastapi import APIRouter, Depends, Request

from app.core.security import get_current_user
from app.i18n import get_language, t
from app.models.user import User

router = APIRouter(prefix="/api/payments", tags=["Pagos (Fase 2)"])


@router.get("/plans")
def get_plans(request: Request, current_user: User = Depends(get_current_user)):
    """Obtener los planes disponibles."""
    lang = get_language(request)
    return {
        "plans": [
            {
                "id": "free",
                "name": t("free_plan", lang),
                "price": 0,
                "currency": "ARS",
                "features": [
                    t("register_3_dogs", lang),
                    t("3_verifications_day", lang),
                    t("basic_qr", lang),
                    t("vaccine_record", lang),
                ],
            },
            {
                "id": "premium",
                "name": t("premium_plan", lang),
                "price": 2999,
                "currency": "ARS",
                "features": [
                    t("unlimited_dogs", lang),
                    t("unlimited_verifications", lang),
                    t("custom_qr", lang),
                    t("vaccine_record", lang),
                    t("priority_support", lang),
                    t("pdf_export", lang),
                ],
            },
        ],
        "message": t("payments_coming_soon", lang),
    }


@router.post("/checkout")
def create_checkout(request: Request, current_user: User = Depends(get_current_user)):
    """Crear sesión de pago (placeholder)."""
    lang = get_language(request)
    return {
        "message": t("mercadopago_coming_soon", lang),
        "status": "not_implemented",
    }
