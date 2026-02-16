"""
Internationalization (i18n) module for IdentiCan backend.
Provides multi-language support for API responses via Accept-Language header.
Supported languages: es (Spanish), en (English), pt (Portuguese).
"""

from fastapi import Request

TRANSLATIONS = {
    "es": {
        # Auth
        "account_exists": "Ya existe una cuenta con este email",
        "password_min_length": "La contraseña debe tener al menos 6 caracteres",
        "invalid_credentials": "Email o contraseña incorrectos",
        # Dogs
        "dog_not_found": "Perro no encontrado",
        "dog_no_access": "No tenés acceso a este perro",
        "dog_only_owner_edit": "Solo el dueño puede editar",
        "dog_only_owner_delete": "Solo el dueño puede eliminar",
        # Vaccines
        "vaccine_not_found": "Vacuna no encontrada",
        "vaccine_no_access": "No tenés acceso a esta vacuna",
        # Nose
        "daily_limit_reached": "Límite diario alcanzado",
        "upgrade_premium": "Upgrade a Premium para verificaciones ilimitadas",
        "max_images": "Máximo 3 imágenes permitidas",
        "file_not_image": "El archivo {filename} no es una imagen",
        "nose_images_uploaded": "Imágenes de nariz subidas correctamente",
        "must_be_image": "El archivo debe ser una imagen",
        "match_found": "Se encontró una coincidencia",
        "no_match_found": "No se encontró coincidencia",
        # Payments
        "free_plan": "Gratuito",
        "premium_plan": "Premium",
        "register_3_dogs": "Registro de hasta 3 perros",
        "3_verifications_day": "3 verificaciones por día",
        "basic_qr": "QR básico",
        "vaccine_record": "Registro de vacunas",
        "unlimited_dogs": "Perros ilimitados",
        "unlimited_verifications": "Verificaciones ilimitadas",
        "custom_qr": "QR personalizado",
        "priority_support": "Soporte prioritario",
        "pdf_export": "Exportación PDF",
        "payments_coming_soon": "Integración de pagos disponible próximamente",
        "mercadopago_coming_soon": "La integración con Mercado Pago estará disponible próximamente",
    },
    "en": {
        # Auth
        "account_exists": "An account with this email already exists",
        "password_min_length": "Password must be at least 6 characters",
        "invalid_credentials": "Invalid email or password",
        # Dogs
        "dog_not_found": "Dog not found",
        "dog_no_access": "You do not have access to this dog",
        "dog_only_owner_edit": "Only the owner can edit",
        "dog_only_owner_delete": "Only the owner can delete",
        # Vaccines
        "vaccine_not_found": "Vaccine not found",
        "vaccine_no_access": "You do not have access to this vaccine",
        # Nose
        "daily_limit_reached": "Daily limit reached",
        "upgrade_premium": "Upgrade to Premium for unlimited verifications",
        "max_images": "Maximum 3 images allowed",
        "file_not_image": "File {filename} is not an image",
        "nose_images_uploaded": "Nose images uploaded successfully",
        "must_be_image": "File must be an image",
        "match_found": "A match was found",
        "no_match_found": "No match found",
        # Payments
        "free_plan": "Free",
        "premium_plan": "Premium",
        "register_3_dogs": "Register up to 3 dogs",
        "3_verifications_day": "3 verifications per day",
        "basic_qr": "Basic QR",
        "vaccine_record": "Vaccine records",
        "unlimited_dogs": "Unlimited dogs",
        "unlimited_verifications": "Unlimited verifications",
        "custom_qr": "Custom QR",
        "priority_support": "Priority support",
        "pdf_export": "PDF export",
        "payments_coming_soon": "Payment integration coming soon",
        "mercadopago_coming_soon": "Mercado Pago integration will be available soon",
    },
    "pt": {
        # Auth
        "account_exists": "Já existe uma conta com este email",
        "password_min_length": "A senha deve ter pelo menos 6 caracteres",
        "invalid_credentials": "Email ou senha inválidos",
        # Dogs
        "dog_not_found": "Cão não encontrado",
        "dog_no_access": "Você não tem acesso a este cão",
        "dog_only_owner_edit": "Apenas o dono pode editar",
        "dog_only_owner_delete": "Apenas o dono pode excluir",
        # Vaccines
        "vaccine_not_found": "Vacina não encontrada",
        "vaccine_no_access": "Você não tem acesso a esta vacina",
        # Nose
        "daily_limit_reached": "Limite diário atingido",
        "upgrade_premium": "Faça upgrade para Premium para verificações ilimitadas",
        "max_images": "Máximo de 3 imagens permitidas",
        "file_not_image": "O arquivo {filename} não é uma imagem",
        "nose_images_uploaded": "Imagens do nariz enviadas com sucesso",
        "must_be_image": "O arquivo deve ser uma imagem",
        "match_found": "Uma correspondência foi encontrada",
        "no_match_found": "Nenhuma correspondência encontrada",
        # Payments
        "free_plan": "Gratuito",
        "premium_plan": "Premium",
        "register_3_dogs": "Registro de até 3 cães",
        "3_verifications_day": "3 verificações por dia",
        "basic_qr": "QR básico",
        "vaccine_record": "Registro de vacinas",
        "unlimited_dogs": "Cães ilimitados",
        "unlimited_verifications": "Verificações ilimitadas",
        "custom_qr": "QR personalizado",
        "priority_support": "Suporte prioritário",
        "pdf_export": "Exportação PDF",
        "payments_coming_soon": "Integração de pagamentos disponível em breve",
        "mercadopago_coming_soon": "A integração com Mercado Pago estará disponível em breve",
    },
}

DEFAULT_LANGUAGE = "es"
SUPPORTED_LANGUAGES = {"es", "en", "pt"}


def get_language(request: Request) -> str:
    """Extract preferred language from Accept-Language header."""
    accept = request.headers.get("Accept-Language", DEFAULT_LANGUAGE)
    # Parse simple Accept-Language: "en", "pt-BR", "es-AR,es;q=0.9,en;q=0.8"
    for part in accept.split(","):
        lang = part.strip().split(";")[0].strip().split("-")[0].lower()
        if lang in SUPPORTED_LANGUAGES:
            return lang
    return DEFAULT_LANGUAGE


def t(key: str, lang: str = DEFAULT_LANGUAGE, **kwargs) -> str:
    """Translate a key to the given language with optional interpolation."""
    translations = TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LANGUAGE])
    text = translations.get(key, TRANSLATIONS[DEFAULT_LANGUAGE].get(key, key))
    if kwargs:
        text = text.format(**kwargs)
    return text
