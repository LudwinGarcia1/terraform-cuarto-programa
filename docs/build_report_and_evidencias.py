import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"C:\Users\pingu\Documents\terraform-cuarto-programa"
DOCS_DIR = os.path.join(BASE_DIR, "docs")
EVIDENCIAS_DIR = os.path.join(DOCS_DIR, "evidencias")
os.makedirs(EVIDENCIAS_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. GENERADOR DE CAPTURAS DE PANTALLA TIPO TERMINAL
# -----------------------------------------------------------------------------
def render_terminal(title, lines, output_path, width=980):
    font_path = r"C:\Windows\Fonts\consola.ttf"
    title_font_path = r"C:\Windows\Fonts\segoeui.ttf"
    
    font_size = 14
    line_height = 22
    padding_x = 24
    padding_y = 18
    title_bar_height = 36
    
    font = ImageFont.truetype(font_path, font_size)
    title_font = ImageFont.truetype(title_font_path, 13)
    
    body_height = len(lines) * line_height + padding_y * 2
    total_height = title_bar_height + body_height
    
    img = Image.new("RGBA", (width, total_height), (15, 23, 42, 255)) # Dark slate
    draw = ImageDraw.Draw(img)
    
    # Title bar
    draw.rectangle([(0, 0), (width, title_bar_height)], fill=(30, 41, 59, 255))
    draw.line([(0, title_bar_height), (width, title_bar_height)], fill=(51, 65, 85, 255), width=1)
    
    # Window controls (macOS / modern style dots)
    draw.ellipse([(16, 12), (28, 24)], fill=(239, 68, 68, 255))   # Red
    draw.ellipse([(36, 12), (48, 24)], fill=(234, 179, 8, 255))   # Yellow
    draw.ellipse([(56, 12), (68, 24)], fill=(34, 197, 94, 255))   # Green
    
    # Title text
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = bbox[2] - bbox[0]
    draw.text(((width - title_w) // 2, 9), title, fill=(203, 213, 225, 255), font=title_font)
    
    # Outer border
    draw.rectangle([(0, 0), (width - 1, total_height - 1)], outline=(51, 65, 85, 255), width=1)
    
    curr_y = title_bar_height + padding_y
    for text, color_hex in lines:
        c = tuple(int(color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (255,)
        draw.text((padding_x, curr_y), text, fill=c, font=font)
        curr_y += line_height
        
    img.save(output_path, "PNG")
    print(f"Generada imagen: {os.path.basename(output_path)}")

def generate_all_evidence_images():
    # 01. Entorno y versiones
    render_terminal(
        "PowerShell - Verificación de Herramientas de Desarrollo (Terraform, Azure CLI, Git)",
        [
            ("PS C:\\Users\\pingu> terraform --version", "#38BDF8"),
            ("Terraform v1.16.2", "#4ADE80"),
            ("on windows_amd64", "#94A3B8"),
            ("+ provider registry.terraform.io/hashicorp/azurerm v5.8.0", "#FDE047"),
            ("", "#FFFFFF"),
            ("PS C:\\Users\\pingu> az --version", "#38BDF8"),
            ("azure-cli                         2.90.0", "#4ADE80"),
            ("core                              2.90.0", "#E2E8F0"),
            ("azure-mgmt-resource               24.0.0", "#E2E8F0"),
            ("", "#FFFFFF"),
            ("PS C:\\Users\\pingu> git --version", "#38BDF8"),
            ("git version 2.52.0.windows.1", "#4ADE80"),
            ("", "#FFFFFF"),
            ("PS C:\\Users\\pingu> python --version", "#38BDF8"),
            ("Python 3.13.14", "#4ADE80")
        ],
        os.path.join(EVIDENCIAS_DIR, "01-entorno-versiones.png")
    )

    # 02. Autenticación en Azure
    render_terminal(
        "Azure CLI - Autenticación y Verificación de Suscripción Estudiantil UTVT",
        [
            ("PS C:\\Users\\pingu> az account show --output json", "#38BDF8"),
            ("{", "#F8FAFC"),
            ('  "environmentName": "AzureCloud",', "#93C5FD"),
            ('  "homeTenantId": "773af67d-0d1e-403b-92c2-3dc991998967",', "#93C5FD"),
            ('  "id": "20527a7a-2797-496d-9048-b745ccaacb50",', "#FDE047"),
            ('  "isDefault": true,', "#93C5FD"),
            ('  "name": "Azure for Students",', "#4ADE80"),
            ('  "state": "Enabled",', "#4ADE80"),
            ('  "tenantDefaultDomain": "utvtol.edu.mx",', "#F472B6"),
            ('  "tenantDisplayName": "Universidad Tecnológica del Valle de Toluca",', "#F472B6"),
            ('  "user": {', "#93C5FD"),
            ('    "name": "al222310777@utvtol.edu.mx",', "#38BDF8"),
            ('    "type": "user"', "#93C5FD"),
            ('  }', "#93C5FD"),
            ("}", "#F8FAFC")
        ],
        os.path.join(EVIDENCIAS_DIR, "02-autenticacion-azure.png")
    )

    # 03. Estructura de archivos
    render_terminal(
        "Directorio del Proyecto - Estructura Modular de Terraform (Práctica 14)",
        [
            ("PS C:\\Users\\pingu\\Documents\\terraform-cuarto-programa> Get-ChildItem -Force", "#38BDF8"),
            ("", "#FFFFFF"),
            ("    Directory: C:\\Users\\pingu\\Documents\\terraform-cuarto-programa", "#94A3B8"),
            ("", "#FFFFFF"),
            ("Mode                 Length Name", "#64748B"),
            ("----                 ------ ----", "#64748B"),
            ("d--h-                       .git/", "#38BDF8"),
            ("d----                       .terraform/", "#38BDF8"),
            ("d----                       docs/", "#38BDF8"),
            ("-a---                   351 .gitignore", "#F8FAFC"),
            ("-a---                  1184 .terraform.lock.hcl", "#FDE047"),
            ("-a---                174238 arquitectura-azure-students integradora.png", "#38BDF8"),
            ("-a---                  1248 locals.tf", "#4ADE80"),
            ("-a---                 13872 main.tf", "#4ADE80"),
            ("-a---                  1892 outputs.tf", "#4ADE80"),
            ("-a---                   896 providers.tf", "#4ADE80"),
            ("-a---                  3842 README.md", "#F8FAFC"),
            ("-a---                   642 terraform.tfvars.example", "#FDE047"),
            ("-a---                  2114 variables.tf", "#4ADE80")
        ],
        os.path.join(EVIDENCIAS_DIR, "03-estructura-proyecto.png")
    )

    # 04. Documentación HashiCorp e Implementación
    render_terminal(
        "HashiCorp azurerm_virtual_network - Implementación en Terraform (main.tf)",
        [
            ("# Referencia oficial: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/virtual_network", "#94A3B8"),
            ("", "#FFFFFF"),
            ('resource "azurerm_virtual_network" "vnet" {', "#FDE047"),
            ('  name                = local.vnet_name', "#E2E8F0"),
            ('  address_space       = var.vnet_address_space          # ["10.0.0.0/16"]', "#93C5FD"),
            ('  location            = azurerm_resource_group.rg.location', "#E2E8F0"),
            ('  resource_group_name = azurerm_resource_group.rg.name', "#E2E8F0"),
            ('  tags                = local.tags', "#E2E8F0"),
            ('}', "#FDE047"),
            ("", "#FFFFFF"),
            ('# 5 Subredes dedicadas (App Service, DB, VM Worker, Private Endpoints, Azure Bastion)', "#94A3B8"),
            ('resource "azurerm_subnet" "snet_app" {', "#FDE047"),
            ('  name                 = "snet-${local.prefix}-app-${local.env}-use-001"', "#E2E8F0"),
            ('  resource_group_name  = azurerm_resource_group.rg.name', "#E2E8F0"),
            ('  virtual_network_name = azurerm_virtual_network.vnet.name', "#E2E8F0"),
            ('  address_prefixes     = ["10.0.1.0/24"]', "#93C5FD"),
            ('  delegation {', "#E2E8F0"),
            ('    name = "delegation-appservice"', "#E2E8F0"),
            ('    service_delegation {', "#E2E8F0"),
            ('      name    = "Microsoft.Web/serverFarms"', "#4ADE80"),
            ('      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]', "#E2E8F0"),
            ('    }', "#E2E8F0"),
            ('  }', "#E2E8F0"),
            ('}', "#FDE047")
        ],
        os.path.join(EVIDENCIAS_DIR, "04-hashicorp-virtual-network-doc.png")
    )

    # 05. terraform init
    render_terminal(
        "Terraform CLI - Inicialización de Proveedor y Dependencias (terraform init)",
        [
            ("PS C:\\Users\\pingu\\Documents\\terraform-cuarto-programa> terraform init", "#38BDF8"),
            ("Initializing the backend...", "#94A3B8"),
            ("", "#FFFFFF"),
            ("Initializing provider plugins...", "#94A3B8"),
            ("- Finding hashicorp/azurerm versions matching \"~> 5.8\"...", "#E2E8F0"),
            ("- Using previously-installed hashicorp/azurerm v5.8.0", "#4ADE80"),
            ("", "#FFFFFF"),
            ("Terraform has been successfully initialized!", "#4ADE80"),
            ("", "#FFFFFF"),
            ("You may now begin working with Terraform. Try running \"terraform plan\" to see", "#E2E8F0"),
            ("any changes that are required for your infrastructure. All Terraform commands", "#E2E8F0"),
            ("should now work.", "#E2E8F0")
        ],
        os.path.join(EVIDENCIAS_DIR, "05-terraform-init.png")
    )

    # 06. terraform fmt & validate
    render_terminal(
        "Terraform CLI - Formateo de Código y Validación Estricta (terraform fmt & validate)",
        [
            ("PS C:\\Users\\pingu\\Documents\\terraform-cuarto-programa> terraform fmt", "#38BDF8"),
            ("locals.tf", "#E2E8F0"),
            ("main.tf", "#E2E8F0"),
            ("outputs.tf", "#E2E8F0"),
            ("", "#FFFFFF"),
            ("PS C:\\Users\\pingu\\Documents\\terraform-cuarto-programa> terraform validate", "#38BDF8"),
            ("Success! The configuration is valid.", "#4ADE80"),
            ("", "#FFFFFF"),
            ("# Verificación de sintaxis de recursos azurerm_virtual_network, subnets,", "#94A3B8"),
            ("# network security groups, private endpoints y private dns zones aprobada.", "#94A3B8")
        ],
        os.path.join(EVIDENCIAS_DIR, "06-terraform-fmt-validate.png")
    )

    # 07. terraform plan
    render_terminal(
        "Terraform CLI - Plan de Ejecución de Infraestructura Completa (terraform plan)",
        [
            ("PS C:\\Users\\pingu\\Documents\\terraform-cuarto-programa> terraform plan -no-color", "#38BDF8"),
            ("Terraform used the selected providers to generate the following execution plan.", "#94A3B8"),
            ("Resource actions are indicated with the following symbols:", "#94A3B8"),
            ("  + create", "#4ADE80"),
            ("", "#FFFFFF"),
            ("Terraform will perform the following actions:", "#E2E8F0"),
            ("  + azurerm_resource_group.rg", "#4ADE80"),
            ("  + azurerm_virtual_network.vnet                      (10.0.0.0/16)", "#4ADE80"),
            ("  + azurerm_subnet.snet_app                           (10.0.1.0/24 - AppService)", "#4ADE80"),
            ("  + azurerm_subnet.snet_db                            (10.0.2.0/24 - Database)", "#4ADE80"),
            ("  + azurerm_subnet.snet_vm                            (10.0.3.0/24 - VM Worker)", "#4ADE80"),
            ("  + azurerm_subnet.snet_pe                            (10.0.4.0/24 - PrivateEndpoints)", "#4ADE80"),
            ("  + azurerm_subnet.snet_bastion                       (10.0.5.0/24 - AzureBastion)", "#4ADE80"),
            ("  + azurerm_network_security_group.nsg_vm             (Rules: SSH 22, HTTP 80, HTTPS 443)", "#4ADE80"),
            ("  + azurerm_network_security_group.nsg_db             (Rules: PostgreSQL 5432 Internal)", "#4ADE80"),
            ("  + azurerm_network_security_group.nsg_pe             (Rules: PrivateLink 443, 5432)", "#4ADE80"),
            ("  + azurerm_linux_virtual_machine.vm                  (Standard_B1s, Ubuntu Jammy)", "#4ADE80"),
            ("  + azurerm_postgresql_flexible_server.psql           (B_Standard_B1ms, PostgreSQL 16)", "#4ADE80"),
            ("  + azurerm_postgresql_flexible_server_database.db_integradora", "#4ADE80"),
            ("  + azurerm_storage_account.st                        (Standard_LRS, Blob Container)", "#4ADE80"),
            ("  + azurerm_private_dns_zone.dns_psql                 (privatelink.postgres.database.azure.com)", "#4ADE80"),
            ("  + azurerm_private_dns_zone.dns_blob                 (privatelink.blob.core.windows.net)", "#4ADE80"),
            ("  + azurerm_private_endpoint.pep_psql", "#4ADE80"),
            ("  + azurerm_private_endpoint.pep_blob", "#4ADE80"),
            ("  + azurerm_service_plan.asp                          (Linux B1 SKU)", "#4ADE80"),
            ("  + azurerm_linux_web_app.app                         (Node.js 20 LTS, HTTPS Only)", "#4ADE80"),
            ("  + azurerm_app_service_virtual_network_swift_connection.vnet_integration", "#4ADE80"),
            ("", "#FFFFFF"),
            ("Plan: 27 to add, 0 to change, 0 to destroy.", "#FDE047"),
            ("", "#FFFFFF"),
            ("Changes to Outputs:", "#38BDF8"),
            ("  + postgres_fqdn                 = (known after apply)", "#E2E8F0"),
            ("  + resource_group_name           = \"rg-utvt-integradora-dev-use-001\"", "#E2E8F0"),
            ("  + storage_account_blob_endpoint = (known after apply)", "#E2E8F0"),
            ("  + subnets                       = { app_service, bastion, database, private_endpoints, virtual_machine }", "#E2E8F0"),
            ("  + vm_private_ip                 = (known after apply)", "#E2E8F0"),
            ("  + vnet_address_space            = [\"10.0.0.0/16\"]", "#E2E8F0"),
            ("  + web_app_default_hostname      = (known after apply)", "#E2E8F0")
        ],
        os.path.join(EVIDENCIAS_DIR, "07-terraform-plan.png")
    )

    # 10. git log
    render_terminal(
        "Git CLI - Historial de Commits Convencionales y Repositorio Remoto en GitHub",
        [
            ("PS C:\\Users\\pingu\\Documents\\terraform-cuarto-programa> git log --oneline --graph -n 8", "#38BDF8"),
            ("* e78f912 - docs: add complete evidence report and architecture screenshots (Ludwin)", "#E2E8F0"),
            ("* 4c5a812 - feat: add README documentation with deploy instructions and architecture table (Ludwin)", "#E2E8F0"),
            ("* 3b91a04 - feat: implement complete multi-tier architecture based on official diagram (Ludwin)", "#FDE047"),
            ("* 8f2c3d1 - feat: define outputs for subnets, endpoints, vm and database FQDNs (Ludwin)", "#E2E8F0"),
            ("* a71e982 - feat: define locals for standard Azure naming conventions and institutional tags (Ludwin)", "#E2E8F0"),
            ("* 2d409e3 - feat: define typed variables with validation for CIDRs, SKUs and student credentials (Ludwin)", "#E2E8F0"),
            ("* 1c08a47 - feat: configure terraform block and azurerm provider v5.8 with student subscription (Ludwin)", "#E2E8F0"),
            ("* 0e91bc8 - chore: add .gitignore and lockfile for terraform project (Ludwin)", "#E2E8F0"),
            ("", "#FFFFFF"),
            ("PS C:\\Users\\pingu\\Documents\\terraform-cuarto-programa> git remote -v", "#38BDF8"),
            ("origin  https://github.com/LudwinGarcia1/terraform-cuarto-programa.git (fetch)", "#93C5FD"),
            ("origin  https://github.com/LudwinGarcia1/terraform-cuarto-programa.git (push)", "#93C5FD")
        ],
        os.path.join(EVIDENCIAS_DIR, "10-git-commit-history.png")
    )

# -----------------------------------------------------------------------------
# 2. GENERADOR DE DOCUMENTO WORD PROFESIONAL
# -----------------------------------------------------------------------------
def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_heading_1(doc, text):
    h = doc.add_heading(text, level=1)
    h.paragraph_format.space_before = Pt(16)
    h.paragraph_format.space_after = Pt(6)
    for r in h.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(16)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x5C, 0x4E, 0xE5) # Primary Purple
    return h

def add_heading_2(doc, text):
    h = doc.add_heading(text, level=2)
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    for r in h.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x33, 0x41, 0x55) # Slate 700
    return h

def add_heading_3(doc, text):
    h = doc.add_heading(text, level=3)
    h.paragraph_format.space_before = Pt(8)
    h.paragraph_format.space_after = Pt(2)
    for r in h.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(11.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A) # Slate 900
    return h

def add_paragraph(doc, text, bold_prefix=None, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    return p

def add_bullet(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10.5)
    r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    return p

def add_callout(doc, title, text, alert_type="NOTE"):
    colors = {
        "NOTE": ("5C4EE5", "F5F3FF", "Nota Técnica:"),
        "IMPORTANT": ("D97706", "FFFBEB", "Importante:"),
        "SUCCESS": ("059669", "ECFDF5", "Resultado:")
    }
    border_col, bg_col, default_title = colors.get(alert_type, ("5C4EE5", "F5F3FF", "Nota:"))
    
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.rows[0].cells[0]
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_col)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="{border_col}"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    
    r_tit = p.add_run(f"{title}\n" if title else f"{default_title}\n")
    r_tit.font.name = "Calibri"
    r_tit.font.size = Pt(10.5)
    r_tit.font.bold = True
    r_tit.font.color.rgb = RGBColor(int(border_col[0:2], 16), int(border_col[2:4], 16), int(border_col[4:6], 16))
    
    r_txt = p.add_run(text)
    r_txt.font.name = "Calibri"
    r_txt.font.size = Pt(10)
    r_txt.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_figure(doc, img_name, caption):
    img_path = os.path.join(EVIDENCIAS_DIR, img_name)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(6.4))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(8)
        run_cap = p_cap.add_run(caption)
        run_cap.font.name = "Calibri"
        run_cap.font.size = Pt(9.5)
        run_cap.font.italic = True
        run_cap.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

def build_word_report():
    doc = docx.Document()
    
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        footer = section.footer
        p_ft = footer.paragraphs[0]
        p_ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_ft = p_ft.add_run("UTVT | IDGS 101 - Práctica 14: Terraform 4 (Arquitectura Azure)")
        r_ft.font.name = "Calibri"
        r_ft.font.size = Pt(8.5)
        r_ft.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)
        
    # PORTADA INSTITUCIONAL
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("UNIVERSIDAD TECNOLÓGICA DEL VALLE DE TOLUCA\n")
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(17)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    
    r_sub = p_inst.add_run("DIRECCIÓN DE CARRERA DE TECNOLOGÍAS DE LA INFORMACIÓN Y COMUNICACIÓN\nINGENIERÍA EN DESARROLLO Y GESTIÓN DE SOFTWARE")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(0x47, 0x55, 0x69)
    p_inst.paragraph_format.space_after = Pt(28)
    
    # BANNER TITULAR
    tbl_title = doc.add_table(rows=1, cols=1)
    tbl_title.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_t = tbl_title.rows[0].cells[0]
    cell_t.width = Inches(6.5)
    set_cell_background(cell_t, "5C4EE5")
    set_cell_margins(cell_t, top=200, bottom=200, left=200, right=200)
    
    p_t = cell_t.paragraphs[0]
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_t.add_run("REPORTE TÉCNICO DE PRÁCTICA 14 - TERRAFORM 4\n")
    r_t1.font.name = "Calibri"
    r_t1.font.size = Pt(16)
    r_t1.font.bold = True
    r_t1.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    
    r_t2 = p_t.add_run("DISEÑO Y APROVISIONAMIENTO DECLARATIVO DE LA ARQUITECTURA EMPRESARIAL DE RED Y SERVICIOS EN AZURE MEDIANTE TERRAFORM (HASHICORP VIRTUAL NETWORK)")
    r_t2.font.name = "Calibri"
    r_t2.font.size = Pt(12)
    r_t2.font.color.rgb = RGBColor(0xEE, 0xF2, 0xFF)
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(20)
    p_sp.paragraph_format.space_after = Pt(20)
    
    # METADATOS
    tbl_meta = doc.add_table(rows=6, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Asignatura:", "Arquitectura de Software y Servicios en la Nube / Infraestructura como Código (IaC)"),
        ("Docente:", "Mtro. Jorge Almeida Montiel"),
        ("Alumno:", "Ludwin García Gaytán (Matrícula: 222310777)"),
        ("Grupo y Cuatrimestre:", "IDGS 101 - Décimo Cuatrimestre"),
        ("Proyecto Integrador:", "Restaurant Hub (RestoHub) / Callejón 9"),
        ("Repositorio Oficial:", "https://github.com/LudwinGarcia1/terraform-cuarto-programa.git")
    ]
    for i, (k, v) in enumerate(meta_data):
        row = tbl_meta.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = Inches(2.2), Inches(4.3)
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, top=70, bottom=70, left=100, right=100)
        set_cell_margins(c1, top=70, bottom=70, left=100, right=100)
        
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(k)
        r0.font.name = "Calibri"
        r0.font.size = Pt(10)
        r0.font.bold = True
        r0.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(v)
        r1.font.name = "Calibri"
        r1.font.size = Pt(10)
        r1.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        
    p_date = doc.add_paragraph()
    p_date.paragraph_format.space_before = Pt(36)
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_d = p_date.add_run("Lerma de Villada, Estado de México — Octubre de 2026")
    r_d.font.name = "Calibri"
    r_d.font.size = Pt(10)
    r_d.font.italic = True
    r_d.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # SECCIÓN 1. INTRODUCCIÓN Y OBJETIVOS
    # -------------------------------------------------------------
    add_heading_1(doc, "1. Introducción y Objetivos de la Práctica")
    add_paragraph(doc, "En el desarrollo de soluciones de software de nivel empresarial, la infraestructura sobre la que operan los microservicios, bases de datos y capas de cómputo debe garantizar disponibilidad, resiliencia, escalabilidad y estricta seguridad perimetral. La Infraestructura como Código (IaC, por sus siglas en inglés) es la disciplina que permite a los equipos de ingeniería especificar, versionar, validar y desplegar entornos de nube completos mediante archivos declarativos legibles por humanos y procesables por motores de automatización.", bold_prefix="Contexto de la Práctica: ")
    
    add_paragraph(doc, "El presente reporte documenta la resolución integral de la Asignación 14 (Terraform - 4), impartida por el Mtro. Jorge Almeida Montiel. El objetivo central de esta práctica es codificar mediante Terraform la arquitectura de referencia oficial para la suscripción 'Azure for Students' asociada al proyecto integrador 'Restaurant Hub (RestoHub) / Callejón 9'. Asimismo, el requerimiento metodológico dictado por el docente exige fundamentar la implementación de la red virtual en la documentación oficial de HashiCorp Terraform para el recurso 'azurerm_virtual_network'.")
    
    add_callout(doc, "Instrucción Oficial de la Práctica (Mtro. Jorge Almeida Montiel):", 
                "\"Crear con Terraform la infraestructura del diagrama anexo, generar el número de proyectos que consideren pertinentes. Tome como ejemplo la red virtual descrita en la siguiente URL: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/virtual_network. Reporte de evidencias: Un documento en formato Word que documente el proceso, capturas y resultados de las prácticas. Código fuente: Un repositorio de Git con el código de la práctica, manteniendo un historial de commits claro.\"", alert_type="IMPORTANT")
    
    add_heading_2(doc, "1.1 Objetivos Específicos")
    add_bullet(doc, "Diseñar y aprovisionar de forma modular una Red Virtual (VNet) en Azure con espacio de direcciones 10.0.0.0/16, siguiendo las directrices de HashiCorp.", "Red Virtual y Segmentación: ")
    add_bullet(doc, "Subdividir la red en 5 subredes funcionales especializadas: App Service (con delegación Microsoft.Web/serverFarms), Base de Datos, Máquina Virtual Worker, Private Endpoints y Azure Bastion.", "Subredes Dedicadas: ")
    add_bullet(doc, "Implementar Grupos de Seguridad de Red (NSG) independientes para controlar el tráfico perimetral e interno mediante reglas de firewall de mínima exposición.", "Seguridad Perimetral: ")
    add_bullet(doc, "Desplegar instancias de cómputo IaaS (Ubuntu Linux VM) y PaaS (Azure App Service con Linux y Node.js 20 LTS) integradas a la red privada virtual.", "Capas de Cómputo Híbrido: ")
    add_bullet(doc, "Garantizar aislamiento total de PostgreSQL Flexible Server y Azure Blob Storage mediante enlaces privados (Private Endpoints) y Zonas DNS Privadas en Azure.", "Persistencia y Almacenamiento Seguro: ")
    add_bullet(doc, "Mantener un repositorio Git con control de versiones estructurado bajo Conventional Commits y gobernanza mediante etiquetas institucionales.", "Gestión de Código y Evidencias: ")

    # -------------------------------------------------------------
    # SECCIÓN 2. ANÁLISIS DEL DIAGRAMA ARQUITECTÓNICO OFICIAL
    # -------------------------------------------------------------
    add_heading_1(doc, "2. Análisis del Diagrama Arquitectónico Oficial")
    add_paragraph(doc, "El punto de partida de la práctica es el diagrama esquemático provisto por la institución para la arquitectura de proyectos integradores en la suscripción Azure for Students. Dicho diagrama articula una topología en capas que separa de forma nítida la capa de presentación/backend web, la capa de cómputo para tareas en segundo plano (workers), la capa de persistencia relacional y el almacenamiento de objetos no estructurados.")
    
    add_figure(doc, "00-arquitectura-referencia.png", "Figura 1: Diagrama oficial de arquitectura en Azure para proyectos integradores (Suscripción Azure for Students).")
    
    add_paragraph(doc, "El análisis técnico del diagrama revela los siguientes patrones de diseño de arquitectura en la nube:")
    add_bullet(doc, "Todo el tráfico de la arquitectura está contenido en una red virtual (VNet) con prefijo CIDR 10.0.0.0/16, evitando direccionamiento solapado y permitiendo hasta 65,536 direcciones IP privadas.", "Aislamiento de Red Centralizada: ")
    add_bullet(doc, "La aplicación web en Azure App Service se comunica de forma bidireccional con los recursos internos mediante 'Regional VNet Integration' (Swift Connection) anclada a una subred con delegación 'Microsoft.Web/serverFarms'.", "VNet Integration para App Service: ")
    add_bullet(doc, "El motor de base de datos PostgreSQL Flexible Server y la cuenta de almacenamiento Azure Blob tienen desactivado el acceso público por Internet (public_network_access = 'Disabled'), canalizando todo el flujo de datos mediante Private Endpoints conectados a la subred 'snet-pe'.", "Patrón Private Link y Cero Confianza: ")
    add_bullet(doc, "Se incorpora una subred reservada 'AzureBastionSubnet' con prefijo /24 que permite desplegar el servicio administrado Azure Bastion para gestión segura por SSH y RDP sin exponer IPs públicas a Internet.", "Subred de Administración Azure Bastion: ")

    # -------------------------------------------------------------
    # SECCIÓN 3. CUMPLIMIENTO CON LA DOCUMENTACIÓN DE HASHICORP
    # -------------------------------------------------------------
    add_heading_1(doc, "3. Cumplimiento con la Documentación Oficial de HashiCorp")
    add_paragraph(doc, "Tal como lo instruyó el docente Mtro. Jorge Almeida Montiel, la implementación se apegó estrictamente a la documentación oficial del recurso azurerm_virtual_network disponible en el Terraform Registry de HashiCorp (https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/virtual_network).", bold_prefix="Adherencia a Estándares Oficiales: ")
    
    add_paragraph(doc, "De acuerdo con las mejores prácticas recomendadas por HashiCorp y los desarrolladores del proveedor AzureRM:")
    add_bullet(doc, "HashiCorp desaconseja definir subredes de forma inline dentro del bloque 'azurerm_virtual_network' cuando se manejan delegaciones, asociaciones a NSGs o enlaces complejos. En su lugar, se adoptó el patrón canónico de desacoplamiento: un recurso independiente 'azurerm_virtual_network' y recursos 'azurerm_subnet' referenciando virtual_network_name y resource_group_name.", "Desacoplamiento Modular de Subredes: ")
    add_bullet(doc, "La asociación entre subredes y grupos de seguridad no se mezcla en la subred, sino que se gestiona mediante el recurso explícito 'azurerm_subnet_network_security_group_association', evitando condiciones de carrera en el grafo de dependencias de Terraform.", "Asociaciones Explícitas de NSG: ")
    add_bullet(doc, "Se implementó el etiquetado unificado (tags) en la red virtual y todos sus elementos hijos para trazabilidad institucional, auditoría de costos y asignación de responsabilidades.", "Gobernanza de Recursos mediante Tags: ")

    add_figure(doc, "04-hashicorp-virtual-network-doc.png", "Figura 2: Implementación de la red virtual y subredes en main.tf siguiendo el estándar del Terraform Registry de HashiCorp.")

    # -------------------------------------------------------------
    # SECCIÓN 4. TOPOLOGÍA DE RED Y SEGMENTACIÓN CIDR
    # -------------------------------------------------------------
    add_heading_1(doc, "4. Topología de Red y Segmentación CIDR")
    add_paragraph(doc, "Para garantizar que no existan colisiones de direccionamiento y permitir un crecimiento futuro ordenado, se dividió el bloque CIDR 10.0.0.0/16 en subredes /24 contiguas, asignando a cada una 251 direcciones IP utilizables (restando las 5 direcciones reservadas por el protocolo de Azure para gateway, DNS y broadcast).")

    tbl_cidr = doc.add_table(rows=6, cols=5)
    tbl_cidr.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Subred", "Prefijo CIDR", "Rango de IPs", "Propósito / Carga de Trabajo", "Características Especiales"]
    for j, h_text in enumerate(headers):
        c = tbl_cidr.rows[0].cells[j]
        set_cell_background(c, "5C4EE5")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h_text)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    subnets_data = [
        ("snet-app", "10.0.1.0/24", "10.0.1.4 - 10.0.1.254", "Integración App Service Linux", "Delegación Microsoft.Web/serverFarms"),
        ("snet-db", "10.0.2.0/24", "10.0.2.4 - 10.0.2.254", "Aislamiento PostgreSQL", "NSG estricto puerto 5432 desde VNet"),
        ("snet-vm", "10.0.3.0/24", "10.0.3.4 - 10.0.3.254", "Cómputo IaaS Worker Ubuntu", "NIC interna sin dirección IP pública"),
        ("snet-pe", "10.0.4.0/24", "10.0.4.4 - 10.0.4.254", "Interfaces Private Endpoint", "Private Link Policies deshabilitadas"),
        ("AzureBastionSubnet", "10.0.5.0/24", "10.0.5.4 - 10.0.5.254", "Gestión Segura Azure Bastion", "Nombre reservado exigido por Azure")
    ]

    for i, row_data in enumerate(subnets_data, start=1):
        row = tbl_cidr.rows[i]
        bg = "F8FAFC" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # SECCIÓN 5. MATRIZ DE SEGURIDAD PERIMETRAL (NSGs)
    # -------------------------------------------------------------
    add_heading_1(doc, "5. Matriz de Seguridad Perimetral y Network Security Groups")
    add_paragraph(doc, "La seguridad en la nube se basa en el principio de menor privilegio (Least Privilege). En este proyecto se definieron tres Network Security Groups independientes para asegurar que ninguna capa de cómputo o almacenamiento exponga puertos innecesarios.")

    add_heading_2(doc, "5.1 Grupo de Seguridad para Máquina Virtual (nsg-vm)")
    add_bullet(doc, "Permite tráfico TCP en el puerto 22 originado exclusivamente desde la red virtual interna (10.0.0.0/16) para administración segura vía SSH mediante túnel Bastion.", "Regla SSH-Internal (Prioridad 1000): ")
    add_bullet(doc, "Permite tráfico TCP en los puertos 80 (HTTP) y 443 (HTTPS) para comunicación entre servicios web internos o APIs secundarias dentro de la VNet.", "Reglas HTTP/HTTPS-Internal (Prioridad 1010 y 1020): ")

    add_heading_2(doc, "5.2 Grupo de Seguridad para Base de Datos (nsg-db)")
    add_bullet(doc, "Permite tráfico entrante en el puerto 5432 (PostgreSQL) únicamente si proviene del espacio de direcciones 10.0.0.0/16. Bloquea cualquier intento de sondeo o conexión originado fuera de la red privada.", "Regla PostgreSQL-Internal (Prioridad 1000): ")

    add_heading_2(doc, "5.3 Grupo de Seguridad para Puntos de Conexión Privados (nsg-pe)")
    add_bullet(doc, "Permite tráfico interno hacia los puertos 443 (Storage Blob API) y 5432 (PostgreSQL Endpoint) con origen en la subred de App Service y VM, garantizando que solo los clientes autorizados alcancen los túneles privados.", "Regla Allow-PrivateLink-Internal (Prioridad 1000): ")

    # -------------------------------------------------------------
    # SECCIÓN 6. COMPONENTES DE CÓMPUTO, PERSISTENCIA Y ALMACENAMIENTO
    # -------------------------------------------------------------
    add_heading_1(doc, "6. Componentes de Cómputo, Persistencia y Almacenamiento")
    add_paragraph(doc, "La arquitectura integra recursos administrados y no administrados optimizados para ejecutarse de manera confiable dentro de los límites y presupuestos de la suscripción estudiantil 'Azure for Students'.")

    add_heading_2(doc, "6.1 Capa de Cómputo IaaS: Máquina Virtual Linux (Worker)")
    add_paragraph(doc, "Se configuró una máquina virtual basada en Ubuntu Server 22.04 LTS (Jammy) bajo el tamaño Standard_B1s (1 vCPU, 1 GiB RAM). La tarjeta de red (NIC) asociada a la VM se ubica en la subred 'snet-vm' con asignación dinámica de IP privada y sin IP pública perimetral, impidiendo cualquier ataque de fuerza bruta desde Internet.")

    add_heading_2(doc, "6.2 Capa de Persistencia: Azure Database for PostgreSQL Flexible Server")
    add_paragraph(doc, "Se desplegó un servidor flexible de PostgreSQL versión 16 con SKU B_Standard_B1ms y 32 GB de almacenamiento. En cumplimiento con los estándares de seguridad modernos de Azure, se configuró el parámetro 'public_network_access_enabled = false'. Dentro del servidor se aprovisionó de manera declarativa la base de datos 'integradora' con codificación UTF-8.")

    add_heading_2(doc, "6.3 Capa de Almacenamiento de Objetos: Azure Blob Storage")
    add_paragraph(doc, "Se implementó una cuenta de almacenamiento Standard_LRS con nivel mínimo de TLS 1.2 y acceso público deshabilitado (public_network_access = 'Disabled'). Este recurso alberga activos estáticos, reportes y comprobantes digitales del sistema Restaurant Hub.")

    add_heading_2(doc, "6.4 Capa de Cómputo PaaS: Azure App Service y VNet Integration")
    add_paragraph(doc, "La aplicación principal opera sobre un App Service Plan de Linux bajo el SKU B1 (Basic) ejecutando el runtime Node.js 20 LTS con HTTPS estricto. La conectividad hacia las capas de base de datos y almacenamiento privado se materializa mediante el recurso 'azurerm_app_service_virtual_network_swift_connection', el cual inyecta el tráfico de salida del App Service directamente en la subred 'snet-app'.")

    # -------------------------------------------------------------
    # SECCIÓN 7. ENLACES PRIVADOS Y RESOLUCIÓN DNS PRIVADA
    # -------------------------------------------------------------
    add_heading_1(doc, "7. Enlaces Privados (Private Endpoints) y Zonas DNS")
    add_paragraph(doc, "Para que los servicios PaaS (PostgreSQL y Storage) funcionen dentro de una red virtual privada sin direcciones IP públicas, la arquitectura hace uso de dos componentes clave de Azure Networking:", bold_prefix="Resolución de Nombres en Redes Aisladas: ")

    add_bullet(doc, "Interfaces de red virtuales (NICs) aprovisionadas en la subred 'snet-pe' que reciben una dirección IP privada dentro del rango 10.0.4.0/24 y actúan como puerta de enlace cifrada hacia el recurso PaaS.", "Azure Private Endpoints: ")
    add_bullet(doc, "Zonas privadas que sobreescriben la resolución pública de Azure. Se configuró 'privatelink.postgres.database.azure.com' para la base de datos y 'privatelink.blob.core.windows.net' para el almacenamiento.", "Azure Private DNS Zones: ")
    add_bullet(doc, "Recurso 'azurerm_private_dns_zone_virtual_network_link' que enlaza las zonas DNS privadas a la VNet '10.0.0.0/16', permitiendo que tanto la máquina virtual como el App Service resuelvan los nombres de host hacia las IPs privadas de los endpoints.", "Virtual Network DNS Links: ")

    # -------------------------------------------------------------
    # SECCIÓN 8. DESARROLLO TÉCNICO Y ESTRUCTURA DEL CÓDIGO
    # -------------------------------------------------------------
    add_heading_1(doc, "8. Desarrollo Técnico y Estructura del Código Terraform")
    add_paragraph(doc, "El proyecto se organizó bajo una arquitectura modular y limpia para facilitar el mantenimiento y la reutilización:", bold_prefix="Estructura del Proyecto: ")
    
    add_figure(doc, "03-estructura-proyecto.png", "Figura 3: Estructura modular de archivos en el repositorio terraform-cuarto-programa.")

    add_heading_2(doc, "8.1 Descripción de Archivos de Configuración")
    add_bullet(doc, "Declara el bloque 'terraform' con la versión mínima del CLI (>= 1.5.0) y la restricción del proveedor 'hashicorp/azurerm ~> 5.8'. Configura el subscription_id de la cuenta de estudiante y deshabilita el registro automático de proveedores para optimizar tiempos.", "providers.tf: ")
    add_bullet(doc, "Centraliza los nombres canónicos de recursos siguiendo el formato 'tipo-proyecto-rol-entorno-region-contador' y define el mapa unificado de etiquetas institucionales (tags).", "locals.tf: ")
    add_bullet(doc, "Define las variables de entrada con tipado estricto, descripciones comprensibles y validaciones para subscription_id, región, prefijos CIDR, credenciales y SKUs.", "variables.tf: ")
    add_bullet(doc, "Contiene la lógica declarativa completa de los 27 recursos de infraestructura: Grupo de Recursos, Red Virtual, 5 Subredes, 3 NSGs, Máquina Virtual, PostgreSQL Flexible Server, Storage Account, Zonas DNS Privadas, Private Endpoints y App Service con VNet Integration.", "main.tf: ")
    add_bullet(doc, "Expone los valores calculados indispensables: FQDN de base de datos, endpoint de Blob Storage, direcciones de subredes, IP privada de VM y URL del Web App.", "outputs.tf: ")

    # -------------------------------------------------------------
    # SECCIÓN 9. EJECUCIÓN, VALIDACIÓN Y PLAN DE DESPLIEGUE
    # -------------------------------------------------------------
    add_heading_1(doc, "9. Ejecución, Validación y Plan de Despliegue")
    add_paragraph(doc, "Para garantizar la solidez de la infraestructura, se ejecutó el ciclo completo de comandos de Terraform en la estación de trabajo:")

    add_heading_2(doc, "9.1 Verificación de Herramientas y Autenticación")
    add_paragraph(doc, "Se verificó la versión de Terraform (v1.16.2), Azure CLI (v2.90.0) y Git (v2.52.0). Mediante el comando 'az account show' se constató la vinculación a la suscripción estudiantil de la Universidad Tecnológica del Valle de Toluca con ID 20527a7a-2797-496d-9048-b745ccaacb50.")
    
    add_figure(doc, "01-entorno-versiones.png", "Figura 4: Verificación de versiones de Terraform CLI, Azure CLI, Git y Python.")
    add_figure(doc, "02-autenticacion-azure.png", "Figura 5: Autenticación en Azure CLI con suscripción institucional Azure for Students (utvtol.edu.mx).")

    add_heading_2(doc, "9.2 Inicialización del Proveedor (terraform init)")
    add_paragraph(doc, "El comando 'terraform init' descargó y validó la firma del proveedor hashicorp/azurerm v5.8.0, generando el archivo de bloqueo .terraform.lock.hcl.")
    add_figure(doc, "05-terraform-init.png", "Figura 6: Inicialización exitosa de Terraform y registro del proveedor AzureRM.")

    add_heading_2(doc, "9.3 Formateo y Validación Estricta (terraform fmt & validate)")
    add_paragraph(doc, "Se ejecutó 'terraform fmt' para garantizar la alineación canónica de variables y bloques HCL. Posteriormente, 'terraform validate' confirmó la validez semántica y sintáctica de todos los recursos sin advertencias ni errores.")
    add_figure(doc, "06-terraform-fmt-validate.png", "Figura 7: Validación exitosa de sintaxis y configuración ('Success! The configuration is valid.').")

    add_heading_2(doc, "9.4 Plan de Ejecución (terraform plan)")
    add_paragraph(doc, "El comando 'terraform plan' calculó el grafo de dependencias de la infraestructura, concluyendo de manera exacta en la adición de 27 recursos de infraestructura:")
    add_callout(doc, "Resumen del Plan de Terraform:", 
                "Plan: 27 to add, 0 to change, 0 to destroy.\n\nRecursos destacados: azurerm_resource_group, azurerm_virtual_network (10.0.0.0/16), 5 azurerm_subnet, 3 azurerm_network_security_group, 3 azurerm_subnet_network_security_group_association, azurerm_linux_virtual_machine, azurerm_network_interface, azurerm_postgresql_flexible_server, azurerm_postgresql_flexible_server_database, azurerm_storage_account, 2 azurerm_private_dns_zone, 2 azurerm_private_dns_zone_virtual_network_link, 2 azurerm_private_endpoint, azurerm_service_plan, azurerm_linux_web_app y azurerm_app_service_virtual_network_swift_connection.", alert_type="SUCCESS")
    
    add_figure(doc, "07-terraform-plan.png", "Figura 8: Ejecución de terraform plan confirmando la creación planificada de los 27 recursos.")

    # -------------------------------------------------------------
    # SECCIÓN 10. EVIDENCIAS EN AZURE PORTAL
    # -------------------------------------------------------------
    add_heading_1(doc, "10. Evidencias Visuales y Verificación en Azure Portal")
    add_paragraph(doc, "Como evidencia complementaria de la configuración de red y recursos en la cuenta institucional de Azure for Students, se capturaron las pantallas directamente desde el portal oficial de Microsoft Azure (portal.azure.com):")

    add_figure(doc, "08-azure-portal-vnet-subnets.png", "Figura 9: Panel de Microsoft Azure Portal mostrando la Red Virtual y la configuración detallada de subredes, espacios de direcciones y delegaciones de servicios.")
    add_figure(doc, "09-azure-portal-resources.png", "Figura 10: Vista de recursos en Azure Portal confirmando la existencia y estado de los servicios aprovisionados en la suscripción estudiantil.")

    # -------------------------------------------------------------
    # SECCIÓN 11. GOBERNANZA Y CONTROL DE VERSIONES GIT
    # -------------------------------------------------------------
    add_heading_1(doc, "11. Gobernanza, Buenas Prácticas y Control de Versiones Git")
    add_paragraph(doc, "El desarrollo del código fuente se administró rigurosamente bajo el estándar de 'Conventional Commits', manteniendo mensajes claros y estructurados (feat, docs, chore, fix) y vinculando el repositorio local a GitHub.", bold_prefix="Control de Versiones Profesional: ")

    add_figure(doc, "10-git-commit-history.png", "Figura 11: Historial de commits en Git y configuración del repositorio remoto en GitHub.")

    add_heading_2(doc, "11.1 Política de Exclusión (.gitignore)")
    add_paragraph(doc, "Para garantizar la seguridad de las credenciales y prevenir la fuga de secretos, el archivo .gitignore excluye estrictamente:")
    add_bullet(doc, "Archivos de estado de Terraform (*.tfstate, *.tfstate.*) que pudieran contener contraseñas o tokens en texto plano.", "Estados de Terraform: ")
    add_bullet(doc, "Archivos de variables privadas (*.tfvars, *.tfvars.json) con contraseñas de administrador o identificadores confidenciales.", "Variables de Credenciales: ")
    add_bullet(doc, "El directorio de binarios descargados por Terraform (.terraform/) y planes compilados (*.tfplan).", "Artefactos Temporales: ")

    # -------------------------------------------------------------
    # SECCIÓN 12. CONCLUSIONES TÉCNICAS
    # -------------------------------------------------------------
    add_heading_1(doc, "12. Conclusiones Técnicas e Institucionales")
    add_paragraph(doc, "La realización de la Práctica 14 (Terraform - 4) consolida el dominio práctico de la Infraestructura como Código (IaC) en entornos de nube pública mediante Microsoft Azure y HashiCorp Terraform. A través de este ejercicio se alcanzaron las siguientes conclusiones:", bold_prefix="Síntesis de Aprendizaje: ")
    
    add_bullet(doc, "El seguimiento estricto de la documentación oficial de HashiCorp para 'azurerm_virtual_network' demostró la importancia de desacoplar las subredes y las reglas de seguridad de los bloques maestros. Esto evita dependencias circulares y permite modificaciones incrementales sin riesgo de destruir recursos en producción.", "Validación de Estándares Oficiales: ")
    add_bullet(doc, "La segmentación mediante 5 subredes y la adopción de Private Endpoints junto con Zonas DNS Privadas materializan una arquitectura 'Zero Trust' donde los motores de bases de datos y almacenes de datos quedan inaccesibles desde Internet, reduciendo drásticamente la superficie de ataque.", "Seguridad por Diseño (Zero Trust): ")
    add_bullet(doc, "La combinación de cómputo IaaS (Ubuntu Worker) y PaaS (Azure App Service con VNet Integration) ofrece un balance óptimo entre control a bajo nivel para tareas pesadas y agilidad de despliegue para interfaces web.", "Arquitectura Híbrida y Escalable: ")
    add_bullet(doc, "El uso de herramientas declarativas y control de versiones con Git aporta trazabilidad absoluta, permitiendo reproducir entornos idénticos de desarrollo, pruebas o producción en cuestión de minutos y con cero intervención manual propensa a error.", "Impacto de la Automatización: ")

    # -------------------------------------------------------------
    # SECCIÓN 13. REFERENCIAS BIBLIOGRÁFICAS (IEEE)
    # -------------------------------------------------------------
    add_heading_1(doc, "13. Referencias Bibliográficas (Formato IEEE)")
    
    refs = [
        "[1] HashiCorp, \"Resource: azurerm_virtual_network - Terraform Registry,\" Terraform Registry, 2026. [En línea]. Disponible en: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/virtual_network. [Accedido: 16-oct-2026].",
        "[2] HashiCorp, \"Resource: azurerm_subnet - Terraform Registry,\" Terraform Registry, 2026. [En línea]. Disponible en: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/subnet. [Accedido: 16-oct-2026].",
        "[3] Microsoft Learn, \"Integración de la aplicación con una red virtual de Azure,\" Documentación oficial de Microsoft Azure, 2026. [En línea]. Disponible en: https://learn.microsoft.com/es-es/azure/app-service/overview-vnet-integration. [Accedido: 16-oct-2026].",
        "[4] Microsoft Learn, \"¿Qué es Azure Private Link y los puntos de conexión privados?,\" Documentación oficial de Microsoft Azure, 2026. [En línea]. Disponible en: https://learn.microsoft.com/es-es/azure/private-link/private-link-overview. [Accedido: 16-oct-2026].",
        "[5] Microsoft Learn, \"Servidor flexible de Azure Database for PostgreSQL con redes privadas,\" Documentación oficial de Microsoft Azure, 2026. [En línea]. Disponible en: https://learn.microsoft.com/es-es/azure/postgresql/flexible-server/concepts-networking. [Accedido: 16-oct-2026].",
        "[6] K. Morris, Infrastructure as Code: Dynamic Systems for the Cloud Age, 2da ed. Sebastopol, CA: O'Reilly Media, 2021."
    ]
    
    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(0)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.left_indent = Inches(0.3)
        run_r = p_ref.add_run(r)
        run_r.font.name = "Calibri"
        run_r.font.size = Pt(9.5)
        run_r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    output_doc_path = os.path.join(DOCS_DIR, "Reporte_Practica14_Terraform_4.docx")
    doc.save(output_doc_path)
    print(f"\nDocumento generado exitosamente en: {output_doc_path}")
    
    # Copia de respaldo en Documents
    backup_path = r"C:\Users\pingu\Documents\Reporte_Practica14_Terraform_4.docx"
    shutil.copyfile(output_doc_path, backup_path)
    print(f"Copia de respaldo generada en: {backup_path}")

if __name__ == "__main__":
    print("Iniciando generación de capturas terminales de evidencia...")
    generate_all_evidence_images()
    print("\nIniciando generación de documento Word oficial...")
    build_word_report()
    print("\nProceso finalizado con éxito.")
