# ==============================================================================
# PRÁCTICA 14: TERRAFORM - 4 (ARQUITECTURA DE INFRAESTRUCTURA EN AZURE)
# Diagrama de Referencia: Azure for Students (Landing Zone + Well-Architected)
# Alumno: Ludwin García Gaytán (Matrícula: 222310777) - UTVT IDGS 101
# Docente: Mtro. Jorge Almeida Montiel
# Basado en la documentación oficial de HashiCorp azurerm_virtual_network
# ==============================================================================

# 1. Grupo de Recursos Principal (Landing Zone)
resource "azurerm_resource_group" "rg" {
  name     = local.resource_group_name
  location = local.location
  tags     = local.tags
}

# 2. Red Virtual (Virtual Network)
# Ejemplo tomado de: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/virtual_network
resource "azurerm_virtual_network" "vnet" {
  name                = local.vnet_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = var.vnet_address_space
  tags                = local.tags
}

# ------------------------------------------------------------------------------
# 3. SEGMENTACIÓN DE SUBREDES (TOPOLOGÍA ZERO-TRUST)
# ------------------------------------------------------------------------------

# 3.1 Subred para Integración de App Service (con delegación oficial)
resource "azurerm_subnet" "snet_app" {
  name                 = "snet-${local.prefix}-app-${local.env}-use-001"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = [var.subnet_prefixes["app"]]

  delegation {
    name = "delegation-appservice"
    service_delegation {
      name    = "Microsoft.Web/serverFarms"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

# 3.2 Subred Reservada para Base de Datos Relacional
resource "azurerm_subnet" "snet_db" {
  name                 = "snet-${local.prefix}-db-${local.env}-use-001"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = [var.subnet_prefixes["db"]]
}

# 3.3 Subred para Máquina Virtual (Worker / Backend Asíncrono)
resource "azurerm_subnet" "snet_vm" {
  name                 = "snet-${local.prefix}-vm-${local.env}-use-001"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = [var.subnet_prefixes["vm"]]
}

# 3.4 Subred para Puntos de Conexión Privados (Private Endpoints)
resource "azurerm_subnet" "snet_pe" {
  name                              = "snet-${local.prefix}-pe-${local.env}-use-001"
  resource_group_name               = azurerm_resource_group.rg.name
  virtual_network_name              = azurerm_virtual_network.vnet.name
  address_prefixes                  = [var.subnet_prefixes["pe"]]
  private_endpoint_network_policies = "Disabled"
}

# 3.5 Subred Dedicada para Azure Bastion
resource "azurerm_subnet" "snet_bastion" {
  name                 = "AzureBastionSubnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = [var.subnet_prefixes["bastion"]]
}

# ------------------------------------------------------------------------------
# 4. GRUPOS DE SEGURIDAD DE RED (NETWORK SECURITY GROUPS - NSG)
# ------------------------------------------------------------------------------

# 4.1 NSG para la Subred de Máquina Virtual
resource "azurerm_network_security_group" "nsg_vm" {
  name                = "nsg-${local.prefix}-vm-${local.env}-use-001"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  tags                = local.tags

  security_rule {
    name                       = "Allow-SSH-Internal-VNet"
    priority                   = 1000
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "10.0.0.0/16"
    destination_address_prefix = "*"
  }
}

resource "azurerm_subnet_network_security_group_association" "nsg_assoc_vm" {
  subnet_id                 = azurerm_subnet.snet_vm.id
  network_security_group_id = azurerm_network_security_group.nsg_vm.id
}

# 4.2 NSG para la Subred de Base de Datos
resource "azurerm_network_security_group" "nsg_db" {
  name                = "nsg-${local.prefix}-db-${local.env}-use-001"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  tags                = local.tags

  security_rule {
    name                       = "Allow-PostgreSQL-VNet"
    priority                   = 1000
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "5432"
    source_address_prefix      = "10.0.0.0/16"
    destination_address_prefix = "*"
  }
}

resource "azurerm_subnet_network_security_group_association" "nsg_assoc_db" {
  subnet_id                 = azurerm_subnet.snet_db.id
  network_security_group_id = azurerm_network_security_group.nsg_db.id
}

# 4.3 NSG para la Subred de Private Endpoints
resource "azurerm_network_security_group" "nsg_pe" {
  name                = "nsg-${local.prefix}-pe-${local.env}-use-001"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  tags                = local.tags

  security_rule {
    name                       = "Allow-PrivateLink-Internal"
    priority                   = 1000
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_ranges    = ["443", "5432"]
    source_address_prefix      = "10.0.0.0/16"
    destination_address_prefix = "*"
  }
}

resource "azurerm_subnet_network_security_group_association" "nsg_assoc_pe" {
  subnet_id                 = azurerm_subnet.snet_pe.id
  network_security_group_id = azurerm_network_security_group.nsg_pe.id
}

# ------------------------------------------------------------------------------
# 5. CÓMPUTO: MÁQUINA VIRTUAL LINUX (WORKER)
# ------------------------------------------------------------------------------
resource "azurerm_network_interface" "nic_vm" {
  name                = "nic-${local.prefix}-vm-${local.env}-use-001"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  tags                = local.tags

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.snet_vm.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_linux_virtual_machine" "vm" {
  name                            = local.vm_name
  location                        = azurerm_resource_group.rg.location
  resource_group_name             = azurerm_resource_group.rg.name
  size                            = var.vm_size
  admin_username                  = var.admin_username
  admin_password                  = var.admin_password
  disable_password_authentication = false
  network_interface_ids           = [azurerm_network_interface.nic_vm.id]
  tags                            = local.tags

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }
}

# ------------------------------------------------------------------------------
# 6. PERSISTENCIA: AZURE DATABASE FOR POSTGRESQL FLEXIBLE SERVER
# ------------------------------------------------------------------------------
resource "azurerm_postgresql_flexible_server" "psql" {
  name                          = local.postgres_server_name
  resource_group_name           = azurerm_resource_group.rg.name
  location                      = azurerm_resource_group.rg.location
  version                       = "16"
  administrator_login           = var.admin_username
  administrator_password        = var.admin_password
  sku_name                      = "B_Standard_B1ms"
  storage_mb                    = 32768
  public_network_access_enabled = false
  tags                          = local.tags
}

resource "azurerm_postgresql_flexible_server_database" "db_integradora" {
  name      = "integradora"
  server_id = azurerm_postgresql_flexible_server.psql.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

# 6.1 Zona DNS Privada y Private Endpoint para PostgreSQL
resource "azurerm_private_dns_zone" "dns_psql" {
  name                = "privatelink.postgres.database.azure.com"
  resource_group_name = azurerm_resource_group.rg.name
  tags                = local.tags
}

resource "azurerm_private_dns_zone_virtual_network_link" "dns_link_psql" {
  name                = "vnetlink-psql-utvt"
  private_dns_zone_id = azurerm_private_dns_zone.dns_psql.id
  virtual_network_id  = azurerm_virtual_network.vnet.id
}

resource "azurerm_private_endpoint" "pep_psql" {
  name                = "pep-${local.prefix}-db-${local.env}-use-001"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  subnet_id           = azurerm_subnet.snet_pe.id
  tags                = local.tags

  custom_network_interface_name = "nic-${local.prefix}-pe-db-${local.env}-use-001"

  private_service_connection {
    name                           = "psc-psql-utvt"
    private_connection_resource_id = azurerm_postgresql_flexible_server.psql.id
    subresource_names              = ["postgresqlServer"]
    is_manual_connection           = false
  }

  private_dns_zone_group {
    name                 = "default"
    private_dns_zone_ids = [azurerm_private_dns_zone.dns_psql.id]
  }
}

# ------------------------------------------------------------------------------
# 7. ALMACENAMIENTO DE OBJETOS: AZURE BLOB STORAGE ACCOUNT
# ------------------------------------------------------------------------------
resource "azurerm_storage_account" "st" {
  name                     = local.storage_account_name
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"
  public_network_access    = "Disabled"
  tags                     = local.tags
}

# 7.1 Zona DNS Privada y Private Endpoint para Blob Storage
resource "azurerm_private_dns_zone" "dns_blob" {
  name                = "privatelink.blob.core.windows.net"
  resource_group_name = azurerm_resource_group.rg.name
  tags                = local.tags
}

resource "azurerm_private_dns_zone_virtual_network_link" "dns_link_blob" {
  name                = "vnetlink-blob-utvt"
  private_dns_zone_id = azurerm_private_dns_zone.dns_blob.id
  virtual_network_id  = azurerm_virtual_network.vnet.id
}

resource "azurerm_private_endpoint" "pep_blob" {
  name                = "pep-${local.prefix}-blob-${local.env}-use-001"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  subnet_id           = azurerm_subnet.snet_pe.id
  tags                = local.tags

  custom_network_interface_name = "nic-${local.prefix}-pe-blob-${local.env}-use-001"

  private_service_connection {
    name                           = "psc-blob-utvt"
    private_connection_resource_id = azurerm_storage_account.st.id
    subresource_names              = ["blob"]
    is_manual_connection           = false
  }

  private_dns_zone_group {
    name                 = "default"
    private_dns_zone_ids = [azurerm_private_dns_zone.dns_blob.id]
  }
}

# ------------------------------------------------------------------------------
# 8. CÓMPUTO WEB: APP SERVICE PLAN Y WEB APP CON VNET INTEGRATION
# ------------------------------------------------------------------------------
resource "azurerm_service_plan" "asp" {
  name                = local.app_service_plan_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = var.service_plan_sku
  tags                = local.tags
}

resource "azurerm_linux_web_app" "app" {
  name                = local.web_app_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id     = azurerm_service_plan.asp.id
  https_only          = true
  tags                = local.tags

  site_config {
    always_on           = false
    minimum_tls_version = "1.2"
    ftps_state          = "Disabled"
    application_stack {
      node_version = var.node_version
    }
  }

  app_settings = {
    "DATABASE_HOST"         = "${local.postgres_server_name}.privatelink.postgres.database.azure.com"
    "DATABASE_NAME"         = "integradora"
    "STORAGE_BLOB_ENDPOINT" = azurerm_storage_account.st.primary_blob_endpoint
  }
}

# 8.1 Integración de Red Virtual Swift hacia la subred de App Service
resource "azurerm_app_service_virtual_network_swift_connection" "vnet_integration" {
  app_service_id = azurerm_linux_web_app.app.id
  subnet_id      = azurerm_subnet.snet_app.id
}
