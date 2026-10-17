# Valores comunes para nombrar y etiquetar los recursos del entorno de arquitectura,
# siguiendo las directrices del Cloud Adoption Framework (CAF) y el Well-Architected Framework.
locals {
  location = var.location
  prefix   = "utvt-integradora"
  env      = var.environment

  # Convención estándar de nombres
  resource_group_name   = "rg-${local.prefix}-${local.env}-use-001"
  vnet_name             = "vnet-${local.prefix}-${local.env}-use-001"
  vm_name               = "vm-${local.prefix}-${local.env}-use-001"
  postgres_server_name  = "psql-${local.prefix}-${local.env}-use-001"
  storage_account_name  = "st${replace(local.prefix, "-", "")}${local.env}001"
  app_service_plan_name = "asp-${local.prefix}-${local.env}-use-001"
  web_app_name          = "app-${local.prefix}-web-${local.env}-use-lgg01"

  tags = {
    project     = "Restaurant Hub (RestoHub) / Callejón 9"
    practice    = "14-terraform-4"
    environment = local.env
    owner       = "Ludwin Garcia Gaytan"
    matricula   = "222310777"
    institution = "Universidad Tecnológica del Valle de Toluca (UTVT)"
    career      = "Ingeniería en Desarrollo y Gestión de Software"
    group       = "IDGS 101"
    managed_by  = "terraform"
  }
}
