# Práctica 14: Terraform 4 - Arquitectura Empresarial de Red y Cómputo en Azure

> **Asignatura:** Arquitectura de Software y Servicios en la Nube / Infraestructura como Código (IaC)  
> **Docente:** Mtro. Jorge Almeida Montiel  
> **Alumno:** Ludwin García Gaytán | **Matrícula:** 222310777  
> **Grupo:** IDGS 101 | **Institución:** Universidad Tecnológica del Valle de Toluca (UTVT)  
> **Proyecto:** Restaurant Hub (*RestoHub*) / Callejón 9  
> **Suscripción Azure:** Azure for Students (`20527a7a-2797-496d-9048-b745ccaacb50`)  
> **Región Autorizada:** `eastus` (East US)

---

## 1. Descripción de la Práctica

Esta práctica consiste en el diseño, especificación técnica y aprovisionamiento declarativo de la infraestructura de red, cómputo, persistencia y almacenamiento descrita en el diagrama oficial de arquitectura para proyectos integradores sobre la suscripción **Azure for Students**.

El proyecto se fundamenta directamente en la documentación técnica oficial de HashiCorp para el recurso [`azurerm_virtual_network`](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/virtual_network), implementando segmentación de subredes, grupos de seguridad de red (NSG), zonas DNS privadas, integración de App Service mediante *Regional VNet Integration* y aislamiento estricto de bases de datos relacionales y almacenamiento de objetos mediante *Private Endpoints*.

```
+---------------------------------------------------------------------------------------------------+
| Azure Virtual Network: vnet-utvt-integradora-dev-use-001 (10.0.0.0/16)                             |
|                                                                                                   |
|  [ snet-app ]          [ snet-vm ]           [ snet-db ]         [ snet-pe ]       [ AzureBastion ]|
|  10.0.1.0/24           10.0.3.0/24           10.0.2.0/24         10.0.4.0/24       10.0.5.0/24    |
|  Delegación:           Worker Linux          PostgreSQL Flex     Private Endpoints Bastion Host    |
|  Microsoft.Web/        Ubuntu 22.04 LTS      (Serverless/Flex)   - PostgreSQL DB   Gestión SSH/RDP |
|  serverFarms           NSG: 22, 80, 443      NSG: Port 5432      - Blob Storage    Segura          |
|       │                      │                     ▲                  ▲                   ▲       |
|       │ (VNet Integration)   │ (App Logic)         │ (PrivateLink)    │ (PrivateLink)     │       |
|       ▼                      ▼                     │                  │                   │       |
|  [ Azure App Service: Linux Node.js 20 LTS ]───────┴──────────────────┴───────────────────┘       |
+---------------------------------------------------------------------------------------------------+
```

---

## 2. Componentes de la Arquitectura Implementada

| Recurso | Tipo en Terraform | Especificación / SKU | Segmento CIDR / Función |
| :--- | :--- | :--- | :--- |
| **Resource Group** | `azurerm_resource_group` | N/A | `rg-utvt-integradora-dev-use-001` en `eastus` |
| **Virtual Network** | `azurerm_virtual_network` | Referencia HashiCorp | Espacio de direcciones `10.0.0.0/16` |
| **Subnet App Service** | `azurerm_subnet` | Delegación `Microsoft.Web` | `10.0.1.0/24` (VNet Integration Swift) |
| **Subnet Base de Datos** | `azurerm_subnet` | Aislada con NSG | `10.0.2.0/24` (Tráfico exclusivo PostgreSQL) |
| **Subnet Máquina Virtual** | `azurerm_subnet` | Aislada con NSG | `10.0.3.0/24` (Cómputo worker / backend) |
| **Subnet Private Endpoints** | `azurerm_subnet` | Private Link Services | `10.0.4.0/24` (NICs privadas de DB y Blob) |
| **Subnet Azure Bastion** | `azurerm_subnet` | `AzureBastionSubnet` | `10.0.5.0/24` (Gestión administrativa segura) |
| **NSG Virtual Machine** | `azurerm_network_security_group` | Reglas 22, 80, 443 | Seguridad perimetral para cómputo IaaS |
| **NSG Database** | `azurerm_network_security_group` | Regla 5432 desde VNet | Restricción estricta de tráfico a PostgreSQL |
| **NSG Private Endpoints** | `azurerm_network_security_group` | Reglas 443, 5432 | Control de interfaces Private Link |
| **Linux Virtual Machine** | `azurerm_linux_virtual_machine` | `Standard_B1s` / Ubuntu 22.04 | Nodo de cómputo worker sin IP pública |
| **PostgreSQL Flexible** | `azurerm_postgresql_flexible_server` | `B_Standard_B1ms`, 32GB | Base de datos relacional con acceso público deshabilitado |
| **Blob Storage Account** | `azurerm_storage_account` | `Standard_LRS`, TLS 1.2 | Repositorio de activos sin acceso público |
| **Private DNS Zones** | `azurerm_private_dns_zone` | DNS Privado Azure | Resolución para PostgreSQL y Blob Storage |
| **Private Endpoints** | `azurerm_private_endpoint` | Private Link VNet | Enlace de DB y Storage hacia la subred privada |
| **App Service Linux** | `azurerm_linux_web_app` | `B1` (Basic) / Node 20 LTS | Aplicación web principal con VNet Integration |

---

## 3. Estructura del Repositorio

El proyecto mantiene una estructura modular y declarativa conforme a las mejores prácticas de la industria:

```bash
terraform-cuarto-programa/
├── .gitignore                      # Exclusión de credenciales, tfstate y binarios
├── .terraform.lock.hcl             # Bloqueo determinista de dependencias (azurerm v5.8.0)
├── providers.tf                    # Configuración de Terraform y proveedor azurerm
├── locals.tf                       # Convenciones de nomenclatura y tags institucionales
├── variables.tf                    # Definición de variables de entrada tipadas
├── terraform.tfvars.example        # Plantilla de variables sin secretos
├── main.tf                         # Declaración de VNet, subnets, NSGs, cómputo y servicios
├── outputs.tf                      # Exportación de FQDNs, IPs, subredes y endpoints
├── arquitectura-azure-students...  # Diagrama arquitectónico oficial de referencia
├── README.md                       # Documentación técnica del proyecto
└── docs/
    ├── Reporte_Practica14_Terraform_4.docx   # Reporte formal de evidencias
    └── evidencias/                          # Capturas de ejecución y Azure Portal
        ├── 00-arquitectura-referencia.png
        ├── 01-entorno-versiones.png
        ├── 02-autenticacion-azure.png
        ├── 03-estructura-proyecto.png
        ├── 04-hashicorp-virtual-network-doc.png
        ├── 05-terraform-init.png
        ├── 06-terraform-fmt-validate.png
        ├── 07-terraform-plan.png
        ├── 08-azure-portal-vnet-subnets.png
        └── 09-azure-portal-resources.png
```

---

## 4. Instrucciones de Despliegue y Ejecución

### Prerrequisitos
1. **Terraform CLI**: `v1.16.2` o superior instalado.
2. **Azure CLI**: `v2.90.0` o superior con sesión activa (`az login`).
3. Suscripción activa con autorización en región `eastus`.

### Pasos de Ejecución

1. **Configurar variables locales:**
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Editar terraform.tfvars con la suscripción y credenciales deseadas
   ```

2. **Inicializar el entorno de trabajo:**
   ```bash
   terraform init
   ```

3. **Formatear y validar la sintaxis:**
   ```bash
   terraform fmt
   terraform validate
   ```

4. **Generar y revisar el plan de ejecución:**
   ```bash
   terraform plan -out=tfplan
   ```
   *El plan debe reportar 27 recursos a añadir (`Plan: 27 to add, 0 to change, 0 to destroy`).*

5. **Aprovisionar la infraestructura (opcional):**
   ```bash
   terraform apply tfplan
   ```

6. **Destruir recursos para evitar consumo de crédito:**
   ```bash
   terraform destroy -auto-approve
   ```

---

## 5. Etiquetas Institucionales y Gobernanza

Todos los recursos creados por este módulo heredan automáticamente las siguientes etiquetas de gobernanza en Azure:

- `institution`: Universidad Tecnológica del Valle de Toluca (UTVT)
- `career`: Ingeniería en Desarrollo y Gestión de Software
- `group`: IDGS 101
- `matricula`: 222310777
- `owner`: Ludwin Garcia Gaytan
- `practice`: 14-terraform-4
- `project`: Restaurant Hub (RestoHub) / Callejón 9
- `environment`: dev
- `managed_by`: terraform
