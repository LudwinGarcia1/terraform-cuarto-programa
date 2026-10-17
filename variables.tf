variable "subscription_id" {
  description = "ID de la suscripción de Microsoft Azure (Azure for Students)"
  type        = string
}

variable "location" {
  description = "Región de Azure autorizada para el despliegue de infraestructura"
  type        = string
  default     = "eastus"
}

variable "environment" {
  description = "Identificador del entorno de ciclo de vida (dev, qa, prod)"
  type        = string
  default     = "dev"
}

variable "vnet_address_space" {
  description = "Espacio de direcciones CIDR de la Red Virtual principal"
  type        = list(string)
  default     = ["10.0.0.0/16"]
}

variable "subnet_prefixes" {
  description = "Mapa de prefijos CIDR para las subredes de la arquitectura de referencia"
  type        = map(string)
  default = {
    app     = "10.0.1.0/24"
    db      = "10.0.2.0/24"
    vm      = "10.0.3.0/24"
    pe      = "10.0.4.0/24"
    bastion = "10.0.5.0/24"
  }
}

variable "admin_username" {
  description = "Nombre del usuario administrador de la máquina virtual y base de datos"
  type        = string
  default     = "azureuser"
}

variable "admin_password" {
  description = "Contraseña de administración con complejidad de seguridad"
  type        = string
  default     = "Utvt2026@PasswordSeguro!"
  sensitive   = true
}

variable "vm_size" {
  description = "Tamaño de cómputo para la máquina virtual Linux de background"
  type        = string
  default     = "Standard_B1as_v2"
}

variable "service_plan_sku" {
  description = "Nivel de servicio (SKU) para el App Service Plan en Linux"
  type        = string
  default     = "B1"
}

variable "node_version" {
  description = "Versión del runtime de Node.js para la Web App"
  type        = string
  default     = "20-lts"
}
