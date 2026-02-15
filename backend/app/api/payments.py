"""
Payments API - Placeholder for Mercado Pago integration (FASE 2).

This module provides the endpoint structure for future payment processing.
Currently returns informational responses only.
"""

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/payments", tags=["Pagos (Fase 2)"])


@router.get("/plans")
def get_plans(current_user: User = Depends(get_current_user)):
    """Obtener los planes disponibles."""
    return {
        "plans": [
            {
                "id": "free",
                "name": "Gratuito",
                "price": 0,
                "currency": "ARS",
                "features": [
                    "Registro de hasta 3 perros",
                    "3 verificaciones por día",
                    "QR básico",
                    "Registro de vacunas",
                ],
            },
            {
                "id": "premium",
                "name": "Premium",
                "price": 2999,
                "currency": "ARS",
                "features": [
                    "Perros ilimitados",
                    "Verificaciones ilimitadas",
                    "QR personalizado",
                    "Registro de vacunas",
                    "Soporte prioritario",
                    "Exportación PDF",
                ],
            },
        ],
        "message": "Integración de pagos disponible próximamente",
    }


@router.post("/checkout")
def create_checkout(current_user: User = Depends(get_current_user)):
    """Crear sesión de pago (placeholder)."""
    return {
        "message": "La integración con Mercado Pago estará disponible próximamente",
        "status": "not_implemented",
    }
