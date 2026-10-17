output "resource_group_name" {
  description = "Nombre oficial del Grupo de Recursos aprovisionado"
  value       = azurerm_resource_group.rg.name
}

output "vnet_id" {
  description = "Identificador único de la Red Virtual principal"
  value       = azurerm_virtual_network.vnet.id
}

output "vnet_address_space" {
  description = "Espacio de direccionamiento de la VNet"
  value       = azurerm_virtual_network.vnet.address_space
}

output "subnets" {
  description = "Identificadores de las 5 subredes segmentadas"
  value = {
    app_service       = azurerm_subnet.snet_app.id
    database          = azurerm_subnet.snet_db.id
    virtual_machine   = azurerm_subnet.snet_vm.id
    private_endpoints = azurerm_subnet.snet_pe.id
    bastion           = azurerm_subnet.snet_bastion.id
  }
}

output "vm_private_ip" {
  description = "Dirección IP privada asignada a la Máquina Virtual Linux"
  value       = azurerm_network_interface.nic_vm.private_ip_address
}

output "postgres_fqdn" {
  description = "Nombre de dominio totalmente calificado (FQDN) de PostgreSQL"
  value       = azurerm_postgresql_flexible_server.psql.fqdn
}

output "storage_account_blob_endpoint" {
  description = "Endpoint del servicio Blob Storage"
  value       = azurerm_storage_account.st.primary_blob_endpoint
}

output "web_app_default_hostname" {
  description = "Nombre de dominio público de la Web App"
  value       = azurerm_linux_web_app.app.default_hostname
}
