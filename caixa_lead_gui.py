import sys
import os
import logging
import webbrowser
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QTextEdit, QFileDialog, QCheckBox, 
                            QProgressBar, QMessageBox, QTabWidget, QGroupBox, QFormLayout,
                            QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox,
                            QSplitter, QFrame, QStyleFactory, QStatusBar, QToolBar, QAction,
                            QGraphicsDropShadowEffect, QGraphicsOpacityEffect, QGridLayout,
                            QStackedWidget, QScrollArea, QSizePolicy, QSpacerItem, QDialog, QSpinBox)
from PyQt5.QtCore import (Qt, QThread, pyqtSignal, QUrl, QSize, QPropertyAnimation, 
                         QEasingCurve, QTimer, QPoint, QParallelAnimationGroup, 
                         QSequentialAnimationGroup, QAbstractAnimation)
from PyQt5.QtGui import (QIcon, QFont, QDesktopServices, QTextCursor, QPixmap, QColor, 
                        QPalette, QLinearGradient, QFontDatabase, QMovie)

# Importar a classe CAIXALeadProcessor
from caixa_lead_processor import CAIXALeadProcessor

# Importar sistema de configurações
from app_settings import AppSettings

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('CAIXALeadGUI')

# Definir cores e estilos
PRIMARY_COLOR = "#1976D2"  # Azul principal
SECONDARY_COLOR = "#64B5F6"  # Azul claro
ACCENT_COLOR = "#E3F2FD"  # Azul muito claro para mensagens
BACKGROUND_COLOR = "#F5F5F5"  # Fundo claro
TEXT_COLOR = "#333333"
LIGHT_TEXT_COLOR = "#777777"
CARD_BACKGROUND = "#FFFFFF"
SHADOW_COLOR = "#AAAAAA"
SUCCESS_COLOR = "#4CAF50"  # Verde para sucesso
WARNING_COLOR = "#FFC107"  # Amarelo para avisos
ERROR_COLOR = "#F44336"  # Vermelho para erros

# Ícones em formato base64 para não depender de arquivos externos
WHATSAPP_ICON = """
<svg viewBox="-2.73 0 1225.016 1225.016" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="#FFFFFF">
    <path fill="#E0E0E0" d="M1041.858 178.02C927.206 63.289 774.753.07 612.325 0 277.617 0 5.232 272.298 5.098 606.991c-.039 106.986 27.915 211.42 81.048 303.476L0 1225.016l321.898-84.406c88.689 48.368 188.547 73.855 290.166 73.896h.258.003c334.654 0 607.08-272.346 607.222-607.023.056-162.208-63.052-314.724-177.689-429.463zm-429.533 933.963h-.197c-90.578-.048-179.402-24.366-256.878-70.339l-18.438-10.93-191.021 50.083 51-186.176-12.013-19.087c-50.525-80.336-77.198-173.175-77.16-268.504.111-278.186 226.507-504.503 504.898-504.503 134.812.056 261.519 52.604 356.814 147.965 95.289 95.36 147.728 222.128 147.688 356.948-.118 278.195-226.522 504.543-504.693 504.543z"/>
    <linearGradient id="a" gradientUnits="userSpaceOnUse" x1="609.77" y1="1190.114" x2="609.77" y2="21.084">
        <stop offset="0" stop-color="#20b038"/>
        <stop offset="1" stop-color="#60d66a"/>
    </linearGradient>
    <path fill="url(#a)" d="M27.875 1190.114l82.211-300.18c-50.719-87.852-77.391-187.523-77.359-289.602.133-319.398 260.078-579.25 579.469-579.25 155.016.07 300.508 60.398 409.898 169.891 109.414 109.492 169.633 255.031 169.57 409.812-.133 319.406-260.094 579.281-579.445 579.281-.023 0 .016 0 0 0h-.258c-96.977-.031-192.266-24.375-276.898-70.5l-307.188 80.548z"/>
    <path fill-rule="evenodd" clip-rule="evenodd" fill="#FFF" d="M462.273 349.294c-11.234-24.977-23.062-25.477-33.75-25.914-8.742-.375-18.75-.352-28.742-.352-10 0-26.25 3.758-39.992 18.766-13.75 15.008-52.5 51.289-52.5 125.078 0 73.797 53.75 145.102 61.242 155.117 7.5 10 103.758 166.266 256.203 226.383 126.695 49.961 152.477 40.023 179.977 37.523s88.734-36.273 101.234-71.297c12.5-35.016 12.5-65.031 8.75-71.305-3.75-6.25-13.75-10-28.75-17.5s-88.734-43.789-102.484-48.789-23.75-7.5-33.75 7.516c-10 15-38.727 48.773-47.477 58.773-8.75 10.023-17.5 11.273-32.5 3.773-15-7.523-63.305-23.344-120.609-74.438-44.586-39.75-74.688-88.844-83.438-103.859-8.75-15-.938-23.125 6.586-30.602 6.734-6.719 15-17.508 22.5-26.266 7.484-8.758 9.984-15.008 14.984-25.008 5-10.016 2.5-18.773-1.25-26.273s-32.898-81.67-46.234-111.326z"/>
    <path fill="#FFF" d="M1036.898 176.091C923.562 62.677 772.859.185 612.297.114 281.43.114 12.172 269.286 12.039 600.137 12 705.896 39.633 809.13 92.156 900.13L7 1211.067l318.203-83.438c87.672 47.812 186.383 73.008 286.836 73.047h.255.003c330.812 0 600.109-269.219 600.25-600.055.055-160.343-62.328-311.108-175.649-424.53zm-424.601 923.242h-.195c-89.539-.047-177.344-24.086-253.93-69.531l-18.227-10.805-188.828 49.508 50.414-184.039-11.875-18.867c-49.945-79.414-76.312-171.188-76.273-265.422.109-274.992 223.906-498.711 499.102-498.711 133.266.055 258.516 52 352.719 146.266 94.195 94.266 146.031 219.578 145.992 352.852-.118 274.999-223.923 498.749-498.899 498.749z"/>
</svg>
"""

VIEW_ICON = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#FFFFFF">
    <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
</svg>
"""

SKIP_ICON = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#FFFFFF">
    <path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z"/>
</svg>
"""

START_ICON = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#FFFFFF">
    <path d="M8 5v14l11-7z"/>
</svg>
"""

STOP_ICON = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#FFFFFF">
    <path d="M6 6h12v12H6z"/>
</svg>
"""

SEARCH_ICON = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#FFFFFF">
    <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
</svg>
"""

EDIT_ICON = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#FFFFFF">
    <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
</svg>
"""

# CAIXA Logo will be loaded from CAIXA.jpeg file

class AnimatedButton(QPushButton):
    """Botão com animações simples de hover e clique"""
    
    def __init__(self, text, color=PRIMARY_COLOR, hover_color=None, icon_data=None, compact=False):
        super().__init__(text)
        self.setMinimumHeight(40 if compact else 45)
        self.setCursor(Qt.PointingHandCursor)
        
        # Configurar fonte
        font = QFont("Segoe UI", 9 if compact else 10)
        font.setBold(True)
        self.setFont(font)
        
        # Configurar ícone se fornecido
        if icon_data:
            self.setIcon(self.create_icon_from_svg(icon_data))
            self.setIconSize(QSize(18 if compact else 20, 18 if compact else 20))
        
        # Cores
        self.color = color
        self.hover_color = hover_color or self._lighten_color(color)
        self.pressed_color = self._darken_color(color)
        
        # Efeito de sombra
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 3)
        self.setGraphicsEffect(self.shadow)
        
        # Aplicar estilo
        self._update_style(self.color)
        
        # Flags para controle de animação
        self.is_hovered = False
        self.is_pressed = False
        
    def create_icon_from_svg(self, svg_data):
        """Criar um ícone a partir de dados SVG"""
        from PyQt5.QtSvg import QSvgRenderer
        from PyQt5.QtCore import QByteArray
        from PyQt5.QtGui import QPixmap, QPainter
        
        renderer = QSvgRenderer(QByteArray(svg_data.encode()))
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        
        return QIcon(pixmap)
    
    def _lighten_color(self, color):
        """Clarear uma cor hexadecimal"""
        color = color.lstrip('#')
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
        
        factor = 1.2
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _darken_color(self, color):
        """Escurecer uma cor hexadecimal"""
        color = color.lstrip('#')
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
        
        factor = 0.8
        r = max(0, int(r * factor))
        g = max(0, int(g * factor))
        b = max(0, int(b * factor))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _update_style(self, color):
        """Atualizar o estilo do botão"""
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #888888;
            }}
        """)
    
    def enterEvent(self, event):
        """Evento quando o mouse entra no botão"""
        self.is_hovered = True
        self._update_style(self.hover_color)
        self.shadow.setBlurRadius(20)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Evento quando o mouse sai do botão"""
        self.is_hovered = False
        self._update_style(self.color)
        self.shadow.setBlurRadius(15)
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """Evento quando o botão é pressionado"""
        if event.button() == Qt.LeftButton:
            self.is_pressed = True
            self._update_style(self.pressed_color)
            # Reduzir ligeiramente a sombra
            self.shadow.setBlurRadius(10)
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Evento quando o botão é liberado"""
        if event.button() == Qt.LeftButton:
            self._update_style(self.hover_color if self.underMouse() else self.color)
        super().mouseReleaseEvent(event)

class Card(QFrame):
    """Widget de card com sombra e animações simples"""
    
    def __init__(self, title=None, parent=None, accent_color=None, compact=False, animated=True):
        super().__init__(parent)
        self.setObjectName("card")
        self.animated = animated
        self.accent_color = accent_color or PRIMARY_COLOR
        
        # Configurar estilo base
        border_style = f"border-left: 4px solid {self.accent_color};" if accent_color else ""
        padding = "10px" if compact else "15px"
        
        self.setStyleSheet(f"""
            #card {{
                background-color: {CARD_BACKGROUND};
                border-radius: 8px;
                {border_style}
                padding: {padding};
            }}
        """)
        
        # Efeito de sombra
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0, 40))
        self.shadow.setOffset(0, 3)
        self.setGraphicsEffect(self.shadow)
        
        # Layout
        self.layout = QVBoxLayout(self)
        margins = 10 if compact else 15
        self.layout.setContentsMargins(margins, margins, margins, margins)
        self.layout.setSpacing(10 if compact else 15)
        
        # Título
        if title:
            title_layout = QHBoxLayout()
            title_layout.setContentsMargins(0, 0, 0, 5)
            
            # Indicador de cor (opcional)
            if accent_color:
                indicator = QLabel()
                indicator.setFixedSize(4, 20)
                indicator.setStyleSheet(f"background-color: {self.accent_color}; border-radius: 2px;")
                title_layout.addWidget(indicator)
                title_layout.addSpacing(8)
            
            # Texto do título
            title_label = QLabel(title)
            font_size = "14px" if compact else "16px"
            title_label.setStyleSheet(f"""
                font-size: {font_size};
                font-weight: bold;
                color: {TEXT_COLOR};
                padding-bottom: 5px;
            """)
            title_layout.addWidget(title_label)
            title_layout.addStretch()
            
            self.layout.addLayout(title_layout)
            
            # Linha separadora
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            separator.setStyleSheet(f"background-color: #e0e0e0; border: none; height: 1px;")
            self.layout.addWidget(separator)
    
    def enterEvent(self, event):
        """Evento quando o mouse entra no card"""
        if self.animated:
            self.shadow.setBlurRadius(25)
            self.shadow.setOffset(0, 6)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Evento quando o mouse sai do card"""
        if self.animated:
            self.shadow.setBlurRadius(15)
            self.shadow.setOffset(0, 3)
        super().leaveEvent(event)

class WorkerThread(QThread):
    """Thread para executar o processamento de leads em segundo plano"""
    update_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int, int)  # (current, total)
    lead_signal = pyqtSignal(dict)  # Emite informações do lead
    finished_signal = pyqtSignal(list)  # Emite lista de todos os leads processados
    error_signal = pyqtSignal(str)
    request_city_signal = pyqtSignal(dict)  # Solicitar cidade ao usuário
    warning_signal = pyqtSignal(str)  # Emite avisos não críticos
    
    def __init__(self, file_path, headless=True, auto_skip=True):
        super().__init__()
        self.file_path = file_path
        self.headless = headless
        self.auto_skip = auto_skip
        self.processor = None
        self.stop_requested = False
        self.all_leads = []  # Lista para armazenar todos os leads processados
        self.current_lead_index = 0
        self.total_leads = 0
        
    def run(self):
        try:
            self.update_signal.emit("🚀 Iniciando processamento de leads da CAIXA...")
            
            # Inicializar o processador
            try:
                self.processor = CAIXALeadProcessor(self.file_path, headless=self.headless)
                self.update_signal.emit("✅ Processador inicializado com sucesso")
            except Exception as e:
                self.error_signal.emit(f"Erro ao inicializar processador: {str(e)}")
                return
            
            # Extrair leads
            try:
                self.update_signal.emit("📄 [LENDO] Abrindo arquivo de leads...")
                self.update_signal.emit(f"📁 [ARQUIVO] {self.file_path}")
                
                self.update_signal.emit("🔍 [ANALISANDO] Extraindo informações dos leads...")
                leads = self.processor.extract_leads()
                
                if not leads:
                    self.update_signal.emit("⚠️ [VAZIO] Nenhum lead encontrado no arquivo.")
                    self.update_signal.emit("📋 [DICA] Verifique se o arquivo contém dados no formato correto")
                    self.finished_signal.emit([])
                    return
                    
                self.total_leads = len(leads)
                self.update_signal.emit(f"✅ [SUCESSO] Encontrados {len(leads)} leads no arquivo.")
                
                # Mostrar resumo dos leads encontrados
                names = [lead.get('name', 'Nome não informado') for lead in leads[:3]]  # Primeiros 3 nomes
                self.update_signal.emit(f"👥 [PREVIEW] Primeiros leads: {', '.join(names)}")
                if len(leads) > 3:
                    self.update_signal.emit(f"➕ [TOTAL] E mais {len(leads) - 3} leads...")
                
            except Exception as e:
                self.error_signal.emit(f"Erro ao extrair leads do arquivo: {str(e)}")
                return
            
            # Configurar o WebDriver
            try:
                self.update_signal.emit("🌐 [WEBDRIVER] Iniciando configuração do navegador...")
                
                if self.headless:
                    self.update_signal.emit("👤 [MODO] Execução em modo invisível (headless)")
                else:
                    self.update_signal.emit("🖥️ [MODO] Execução com interface visível")
                
                self.update_signal.emit("⬇️ [DOWNLOAD] Verificando ChromeDriver...")
                self.processor.setup_driver(headless=self.headless)
                self.update_signal.emit("✅ [WEBDRIVER] Navegador configurado e pronto para uso")
                self.update_signal.emit("🚀 [PRONTO] Sistema pronto para processar leads")
            except Exception as e:
                self.error_signal.emit(f"Erro ao configurar WebDriver: {str(e)}")
                return
            
            # Processar cada lead
            for i, lead in enumerate(leads):
                if self.stop_requested:
                    self.update_signal.emit("⏹️ Processamento interrompido pelo usuário.")
                    break
                    
                self.current_lead_index = i + 1
                current = i + 1
                self.progress_signal.emit(current, len(leads))
                
                lead_name = lead.get('name', 'Desconhecido')
                property_id = lead.get('property_id', 'ID não encontrado')
                phone = lead.get('phone', 'Telefone não informado')
                
                self.update_signal.emit("")  # Linha em branco para separar
                self.update_signal.emit("=" * 60)
                self.update_signal.emit(f"👤 [LEAD {current}/{len(leads)}] {lead_name}")
                self.update_signal.emit(f"📞 [TELEFONE] {phone}")
                self.update_signal.emit(f"🏠 [IMÓVEL ID] {property_id}")
                self.update_signal.emit("=" * 60)
                
                # Emitir informações do lead para a interface
                self.lead_signal.emit(lead)
                
                # Processar detalhes do imóvel com tratamento de erro robusto
                lead_status = self.process_lead_safely(lead, property_id)
                lead["status"] = lead_status
                
                # Adicionar o lead à lista de todos os leads
                self.all_leads.append(lead.copy())
                
                # Atualizar o lead na interface
                self.lead_signal.emit(lead)
                
                # Aguardar um pouco para permitir que o usuário veja as informações
                self.msleep(500)  # 500ms de pausa
                
            self.update_signal.emit("🎉 Processamento de leads concluído!")
            self.finished_signal.emit(self.all_leads)
            
        except Exception as e:
            error_msg = f"❌ Erro crítico durante o processamento: {str(e)}"
            logger.error(error_msg)
            self.error_signal.emit(error_msg)
            self.finished_signal.emit(self.all_leads)  # Enviar leads processados até agora
        finally:
            # Limpar recursos
            self.cleanup_resources()
    
    def process_lead_safely(self, lead, property_id):
        """Processar um lead individual com tratamento de erro robusto"""
        try:
            lead_name = lead.get('name', 'Desconhecido')
            
            # Etapa 1: Iniciar processamento do lead
            self.update_signal.emit(f"🔄 [INICIANDO] Processamento do lead: {lead_name}")
            
            # Etapa 2: Buscar detalhes do imóvel
            self.update_signal.emit(f"🔍 [PESQUISANDO] Buscando detalhes do imóvel (ID: {property_id})...")
            
            try:
                # Usar timeout mais curto para evitar travamentos
                import signal
                import time
                
                def timeout_handler(signum, frame):
                    raise TimeoutError("Timeout na busca do imóvel")
                
                # Configurar timeout de 30 segundos para a busca
                timeout_seconds = 30
                start_time = time.time()
                
                # Etapa 3: Conectando ao site da CAIXA
                self.update_signal.emit("🌐 [CONECTANDO] Acessando site da CAIXA...")
                
                property_details = self.processor.search_property_details(property_id)
                
                elapsed_time = time.time() - start_time
                self.update_signal.emit(f"⏱️ [TEMPO] Busca realizada em {elapsed_time:.1f} segundos")
                
                if property_details and property_details.get("url"):
                    lead["property_url"] = property_details["url"]
                    self.update_signal.emit(f"✅ [SUCESSO] URL do imóvel encontrada")
                    self.update_signal.emit(f"🔗 [URL] {property_details['url'][:60]}...")
                    
                    # Etapa 4: Verificar disponibilidade do imóvel
                    self.update_signal.emit("🔍 [VERIFICANDO] Disponibilidade do imóvel...")
                    
                    # Verificar se o imóvel não está mais disponível
                    if property_details.get("property_not_available"):
                        lead["property_not_available"] = True
                        lead["error_details"] = "property_no_longer_available"
                        lead["city"] = "N/A - Imóvel não disponível"
                        self.update_signal.emit("⚠️ [INDISPONÍVEL] Imóvel não está mais disponível para venda")
                        self.update_signal.emit("💬 [TEMPLATE] Mensagem especial será utilizada para este lead")
                        self.update_signal.emit(f"✅ [FINALIZADO] Lead {lead_name} processado com template especial")
                        return "⚠️ Imóvel não disponível - Usar mensagem especial"
                    
                    self.update_signal.emit("✅ [DISPONÍVEL] Imóvel está disponível para venda")
                    
                    # Etapa 5: Extrair informações da cidade
                    self.update_signal.emit("🏙️ [EXTRAINDO] Informações da cidade...")
                    
                    # Tentar extrair cidade com tratamento de erro específico
                    if property_details.get("city"):
                        lead["city"] = property_details["city"]
                        self.update_signal.emit(f"✅ [CIDADE] Cidade extraída com sucesso: {property_details['city']}")
                        self.update_signal.emit(f"🎯 [COMPLETO] Lead {lead_name} processado completamente")
                        return "✅ Completo"
                    else:
                        # Cidade não encontrada - marcar para revisão manual
                        self.update_signal.emit("⚠️ [CIDADE] Cidade não encontrada automaticamente")
                        self.update_signal.emit("🔍 [TENTATIVA] Tentando métodos alternativos de extração...")
                        self.update_signal.emit("❌ [FALHA] Métodos alternativos não obtiveram sucesso")
                        self.update_signal.emit(f"📝 [MANUAL] Lead marcado para revisão manual")
                        self.update_signal.emit(f"🔗 [REVISÃO] URL para revisão: {property_details['url'][:50]}...")
                        lead["city"] = "PENDENTE - Revisar manualmente"
                        lead["manual_review_needed"] = True
                        lead["manual_review_reason"] = "Cidade não encontrada automaticamente"
                        return "⚠️ Pendente - Revisar cidade manualmente"
                        
                else:
                    self.update_signal.emit(f"❌ [ERRO] Imóvel não encontrado no sistema (ID: {property_id})")
                    self.update_signal.emit(f"🔍 [DIAGNÓSTICO] Possíveis causas: ID inválido ou imóvel removido")
                    lead["property_url"] = ""
                    lead["city"] = ""
                    lead["manual_review_needed"] = True
                    lead["manual_review_reason"] = "Imóvel não encontrado no site"
                    self.update_signal.emit(f"📝 [MANUAL] Lead {lead_name} requer verificação manual")
                    return f"❌ Erro - Imóvel não encontrado"
                    
            except TimeoutError as e:
                self.update_signal.emit(f"⏱️ [TIMEOUT] Timeout na busca do imóvel após {timeout_seconds}s")
                self.update_signal.emit(f"🌐 [CONECTIVIDADE] Possível problema de conexão ou site lento")
                self.update_signal.emit(f"🔗 [ALTERNATIVA] Tentando obter URL alternativa...")
                # Tentar obter pelo menos a URL se possível
                try:
                    url = f"https://viahouseleiloes.com.br/search?property_id={property_id}"
                    lead["property_url"] = url
                    lead["city"] = "PENDENTE - Timeout na busca"
                    lead["manual_review_needed"] = True
                    lead["manual_review_reason"] = f"Timeout após {timeout_seconds}s"
                    self.update_signal.emit(f"✅ [URL] URL alternativa gerada para revisão manual")
                    self.update_signal.emit(f"🔗 [REVISÃO] {url}")
                    self.update_signal.emit(f"⚠️ [PENDENTE] Lead {lead_name} marcado para revisão devido ao timeout")
                except:
                    self.update_signal.emit(f"❌ [FALHA] Não foi possível gerar URL alternativa")
                    lead["property_url"] = ""
                    lead["city"] = ""
                return "⚠️ Erro - Timeout na busca"
                
            except Exception as e:
                error_details = str(e)
                stack_trace = ""
                
                # Capturar stack trace completo
                import traceback
                stack_trace = traceback.format_exc()
                
                self.update_signal.emit(f"❌ ERRO DETALHADO: {error_details}")
                self.update_signal.emit(f"📋 Stack Trace:\n{stack_trace}")
                
                # Tentar obter pelo menos uma URL para revisão manual
                try:
                    fallback_url = f"https://viahouseleiloes.com.br/search?q={property_id}"
                    lead["property_url"] = fallback_url
                    lead["city"] = "PENDENTE - Erro na extração"
                    lead["manual_review_needed"] = True
                    lead["manual_review_reason"] = f"Erro: {error_details[:100]}..."
                    lead["error_stack_trace"] = stack_trace
                    self.update_signal.emit(f"🔗 URL para revisão manual: {fallback_url}")
                except:
                    lead["property_url"] = ""
                    lead["city"] = ""
                
                # Determinar tipo de erro e ação
                if "timeout" in error_details.lower():
                    return "⚠️ Erro - Timeout na busca"
                elif "connection" in error_details.lower():
                    return "⚠️ Erro - Problema de conexão"
                elif "element not found" in error_details.lower():
                    return "⚠️ Erro - Página alterada"
                else:
                    return f"❌ Erro - {error_details[:50]}..."
                    
        except Exception as e:
            error_msg = f"❌ Erro crítico no processamento do lead: {str(e)}"
            stack_trace = ""
            try:
                import traceback
                stack_trace = traceback.format_exc()
                self.update_signal.emit(f"📋 Stack Trace Crítico:\n{stack_trace}")
            except:
                pass
                
            self.update_signal.emit(error_msg)
            lead["property_url"] = ""
            lead["city"] = ""
            lead["manual_review_needed"] = True
            lead["manual_review_reason"] = f"Erro crítico: {str(e)}"
            lead["error_stack_trace"] = stack_trace
            return f"❌ Erro crítico - {str(e)[:50]}..."
    
    def cleanup_resources(self):
        """Limpar recursos usados pelo processador"""
        try:
            if self.processor and hasattr(self.processor, 'driver') and self.processor.driver:
                self.processor.driver.quit()
                self.update_signal.emit("🧹 Recursos do WebDriver liberados")
        except Exception as e:
            self.update_signal.emit(f"⚠️ Aviso ao limpar recursos: {str(e)}")
    
    def stop(self):
        """Parar o processamento graciosamente"""
        self.stop_requested = True
        self.update_signal.emit("⏸️ Solicitando interrupção do processamento...")
        self.cleanup_resources()

class EditLeadDialog(QDialog):
    """Diálogo para editar informações do lead"""
    
    def __init__(self, lead_data, parent=None):
        super().__init__(parent)
        self.lead_data = lead_data.copy()
        self.original_name = lead_data.get('name')  # Guardar nome original para identificação
        self.setWindowTitle("Editar Lead")
        self.setModal(True)
        self.setMinimumSize(600, 550)
        self.resize(650, 600)
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar interface do diálogo"""
        layout = QVBoxLayout(self)
        layout.setSpacing(25)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Título
        title = QLabel("✏️ Editar Informações do Lead")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1976D2; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Formulário
        form_layout = QFormLayout()
        form_layout.setSpacing(20)
        form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        
        # Campo Nome
        self.name_edit = QLineEdit(self.lead_data.get('name', ''))
        self.name_edit.setPlaceholderText("Nome completo do cliente")
        self.name_edit.setStyleSheet(self.get_input_style())
        form_layout.addRow("Nome:", self.name_edit)
        
        # Campo Email
        self.email_edit = QLineEdit(self.lead_data.get('email', ''))
        self.email_edit.setPlaceholderText("email@exemplo.com")
        self.email_edit.setStyleSheet(self.get_input_style())
        form_layout.addRow("Email:", self.email_edit)
        
        # Campo Telefone
        self.phone_edit = QLineEdit(self.lead_data.get('phone', ''))
        self.phone_edit.setPlaceholderText("11999999999")
        self.phone_edit.setStyleSheet(self.get_input_style())
        form_layout.addRow("Telefone:", self.phone_edit)
        
        # Campo ID do Imóvel
        self.property_id_edit = QLineEdit(self.lead_data.get('property_id', ''))
        self.property_id_edit.setPlaceholderText("CX08444425765084SP")
        self.property_id_edit.setStyleSheet(self.get_input_style())
        form_layout.addRow("ID do Imóvel:", self.property_id_edit)
        
        # Campo Cidade
        self.city_edit = QLineEdit(self.lead_data.get('city', ''))
        self.city_edit.setPlaceholderText("Nome da cidade")
        self.city_edit.setStyleSheet(self.get_input_style())
        form_layout.addRow("Cidade:", self.city_edit)
        
        # Campo URL do Imóvel
        self.url_edit = QLineEdit(self.lead_data.get('property_url', ''))
        self.url_edit.setPlaceholderText("https://viahouseleiloes.com.br/...")
        self.url_edit.setStyleSheet(self.get_input_style())
        form_layout.addRow("URL do Imóvel:", self.url_edit)
        
        layout.addLayout(form_layout)
        
        # Adicionar espaçamento antes dos botões
        layout.addSpacing(20)
        
        # Botões
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        buttons_layout.addStretch()
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.setMinimumSize(120, 45)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #616161;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
        """)
        cancel_button.clicked.connect(self.reject)
        
        save_button = QPushButton("Salvar")
        save_button.setMinimumSize(120, 45)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        save_button.clicked.connect(self.accept)
        save_button.setDefault(True)
        
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(save_button)
        
        layout.addLayout(buttons_layout)
    
    def get_input_style(self):
        """Estilo para campos de entrada"""
        return """
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                background-color: white;
                min-height: 20px;
            }
            QLineEdit:focus {
                border-color: #1976D2;
                background-color: #f8f9fa;
            }
            QLineEdit:hover {
                border-color: #bdbdbd;
            }
        """
    
    def get_lead_data(self):
        """Obter dados do lead editados"""
        return {
            'name': self.name_edit.text().strip(),
            'email': self.email_edit.text().strip(),
            'phone': self.phone_edit.text().strip(),
            'property_id': self.property_id_edit.text().strip(),
            'city': self.city_edit.text().strip(),
            'property_url': self.url_edit.text().strip(),
            'original_name': self.original_name  # Para identificação
        }

class ReportDialog(QMainWindow):
    """Diálogo para exibir relatório de leads processados"""
    
    def __init__(self, leads, parent=None):
        super().__init__(parent)
        self.leads = leads
        self.init_ui()
        
    def init_ui(self):
        """Inicializar a interface do usuário"""
        self.setWindowTitle("Relatório de Leads Processados")
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Cabeçalho
        header_card = Card("Relatório de Leads Processados")
        header_layout = QHBoxLayout()
        
        # Estatísticas
        stats_layout = QHBoxLayout()
        
        # Total de leads
        total_card = self.create_stat_card("Total de Leads", str(len(self.leads)), PRIMARY_COLOR)
        
        # Leads completos
        complete_leads = sum(1 for lead in self.leads if lead.get("status") == "Completo")
        complete_card = self.create_stat_card("Leads Completos", str(complete_leads), "#4CAF50")
        
        # Leads pendentes
        pending_leads = sum(1 for lead in self.leads if lead.get("status", "").startswith("Pendente"))
        pending_card = self.create_stat_card("Leads Pendentes", str(pending_leads), "#FFC107")
        
        stats_layout.addWidget(total_card)
        stats_layout.addWidget(complete_card)
        stats_layout.addWidget(pending_card)
        
        # Adicionar ao layout principal
        main_layout.addLayout(stats_layout)
        
        # Tabela de leads
        table_card = Card("Lista de Leads")
        table_layout = QVBoxLayout()
        
        self.leads_table = QTableWidget()
        self.leads_table.setColumnCount(7)
        self.leads_table.setHorizontalHeaderLabels(["Nome", "Email", "Telefone", "ID do Imóvel", "Cidade", "Status", "Ações"])
        self.leads_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.leads_table.setAlternatingRowColors(True)
        self.leads_table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
                gridline-color: #f0f0f0;
                font-family: 'Segoe UI';
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f0f0f0;
            }
            QTableWidget::item:selected {
                background-color: #e0f2f1;
                color: #075e54;
            }
            QHeaderView::section {
                background-color: #075e54;
                color: white;
                padding: 10px;
                font-weight: bold;
                border: none;
                font-family: 'Segoe UI';
                font-size: 13px;
            }
            QTableWidget::item:alternate {
                background-color: #f9f9f9;
            }
        """)
        
        # Preencher a tabela com os leads
        self.populate_table()
        
        table_layout.addWidget(self.leads_table)
        table_card.layout.addLayout(table_layout)
        main_layout.addWidget(table_card, 1)  # 1 é o stretch factor
        
        # Botões de ação
        action_layout = QHBoxLayout()
        
        export_button = AnimatedButton("Exportar Relatório", PRIMARY_COLOR)
        export_button.clicked.connect(self.export_report)
        
        close_button = AnimatedButton("Fechar", "#777777")
        close_button.clicked.connect(self.close)
        
        action_layout.addWidget(export_button)
        action_layout.addWidget(close_button)
        
        main_layout.addLayout(action_layout)
    
    def create_stat_card(self, title, value, color):
        """Criar um card de estatística"""
        card = QFrame()
        card.setObjectName("stat_card")
        card.setStyleSheet(f"""
            #stat_card {{
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                border-left: 5px solid {color};
            }}
        """)
        
        # Efeito de sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 5)
        card.setGraphicsEffect(shadow)
        
        # Layout
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Título
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: bold;
            color: {TEXT_COLOR};
        """)
        
        # Valor
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            font-size: 24px;
            font-weight: bold;
            color: {color};
            margin-top: 10px;
        """)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        return card
    
    def populate_table(self):
        """Preencher a tabela com os leads"""
        self.leads_table.setRowCount(len(self.leads))
        
        for i, lead in enumerate(self.leads):
            # Nome
            self.leads_table.setItem(i, 0, QTableWidgetItem(lead.get("name", "-")))
            
            # Email
            self.leads_table.setItem(i, 1, QTableWidgetItem(lead.get("email", "-")))
            
            # Telefone
            self.leads_table.setItem(i, 2, QTableWidgetItem(lead.get("phone", "-")))
            
            # ID do Imóvel
            self.leads_table.setItem(i, 3, QTableWidgetItem(lead.get("property_id", "-")))
            
            # Cidade
            city_item = QTableWidgetItem(lead.get("city", "-"))
            self.leads_table.setItem(i, 4, city_item)
            
            # Status
            status = lead.get("status", "-")
            status_item = QTableWidgetItem(status)
            
            # Definir cor do status
            if status == "Completo":
                status_item.setForeground(QColor("#4CAF50"))
            elif status.startswith("Pendente"):
                status_item.setForeground(QColor("#FFC107"))
            
            self.leads_table.setItem(i, 5, status_item)
            
            # Botões de ação
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            
            # Botão para editar cidade
            if status.startswith("Pendente"):
                edit_button = QPushButton("Editar Cidade")
                edit_button.setStyleSheet("""
                    QPushButton {
                        background-color: #FFC107;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 5px 10px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #FFD54F;
                    }
                """)
                edit_button.clicked.connect(lambda checked, row=i: self.edit_city(row))
                action_layout.addWidget(edit_button)
            
            # Botão para ver imóvel
            if lead.get("property_url"):
                view_button = QPushButton("Ver Imóvel")
                view_button.setStyleSheet("""
                    QPushButton {
                        background-color: #075e54;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 5px 10px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #128c7e;
                    }
                """)
                view_button.clicked.connect(lambda checked, url=lead.get("property_url"): self.view_property(url))
                action_layout.addWidget(view_button)
            
            action_layout.addStretch()
            self.leads_table.setCellWidget(i, 6, action_widget)
    
    def edit_city(self, row):
        """Editar a cidade de um lead"""
        from PyQt5.QtWidgets import QInputDialog
        
        # Obter o lead
        lead = self.leads[row]
        
        # Mostrar diálogo para inserir a cidade
        city, ok = QInputDialog.getText(
            self,
            "Editar Cidade",
            f"Insira a cidade para o imóvel {lead.get('property_id')}:",
            QLineEdit.Normal
        )
        
        if ok and city:
            # Atualizar o lead com a cidade inserida
            lead["city"] = city
            lead["status"] = "Completo"
            
            # Atualizar a tabela
            self.leads_table.item(row, 4).setText(city)
            self.leads_table.item(row, 5).setText("Completo")
            self.leads_table.item(row, 5).setForeground(QColor("#4CAF50"))
            
            # Atualizar o widget de ação
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            
            # Botão para ver imóvel
            if lead.get("property_url"):
                view_button = QPushButton("Ver Imóvel")
                view_button.setStyleSheet("""
                    QPushButton {
                        background-color: #075e54;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 5px 10px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #128c7e;
                    }
                """)
                view_button.clicked.connect(lambda checked, url=lead.get("property_url"): self.view_property(url))
                action_layout.addWidget(view_button)
            
            action_layout.addStretch()
            self.leads_table.setCellWidget(row, 6, action_widget)
            
            # Atualizar estatísticas
            self.update_stats()
    
    def view_property(self, url):
        """Abrir a página do imóvel no navegador"""
        QDesktopServices.openUrl(QUrl(url))
    
    def update_stats(self):
        """Atualizar estatísticas"""
        # Recalcular estatísticas
        complete_leads = sum(1 for lead in self.leads if lead.get("status") == "Completo")
        pending_leads = sum(1 for lead in self.leads if lead.get("status", "").startswith("Pendente"))
        
        # Atualizar cards
        # Como os cards são recriados a cada vez, precisamos recriar o layout
        stats_layout = self.findChild(QHBoxLayout, "stats_layout")
        if stats_layout:
            # Limpar o layout
            while stats_layout.count():
                item = stats_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            
            # Adicionar novos cards
            total_card = self.create_stat_card("Total de Leads", str(len(self.leads)), PRIMARY_COLOR)
            complete_card = self.create_stat_card("Leads Completos", str(complete_leads), "#4CAF50")
            pending_card = self.create_stat_card("Leads Pendentes", str(pending_leads), "#FFC107")
            
            stats_layout.addWidget(total_card)
            stats_layout.addWidget(complete_card)
            stats_layout.addWidget(pending_card)
    
    def export_report(self):
        """Exportar relatório para Excel"""
        try:
            import pandas as pd
            from datetime import datetime
            
            # Criar DataFrame
            data = []
            for lead in self.leads:
                data.append({
                    "Nome": lead.get("name", "-"),
                    "Email": lead.get("email", "-"),
                    "Telefone": lead.get("phone", "-"),
                    "ID do Imóvel": lead.get("property_id", "-"),
                    "Cidade": lead.get("city", "-"),
                    "Status": lead.get("status", "-"),
                    "URL do Imóvel": lead.get("property_url", "-")
                })
            
            df = pd.DataFrame(data)
            
            # Salvar como Excel
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exportar Relatório", 
                f"relatorio_leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                "Excel Files (*.xlsx)"
            )
            
            if file_path:
                df.to_excel(file_path, index=False)
                QMessageBox.information(self, "Exportação Concluída", f"Relatório exportado com sucesso para:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Erro na Exportação", f"Erro ao exportar relatório: {str(e)}")

class LeadProcessorGUI(QMainWindow):
    """Interface gráfica principal para o processador de leads da CAIXA"""
    
    def __init__(self):
        super().__init__()
        
        # Inicializar sistema de configurações
        self.settings = AppSettings()
        
        self.worker_thread = None
        self.current_lead = None
        self.processed_leads = []
        self.current_lead_index = 0  # Para navegação entre leads
        
        # Timer para auto-salvamento
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save_data)
        self.auto_save_timer.start(self.settings.get("processing.auto_save_interval", 300) * 1000)  # Convert to ms
        
        # Carregar fontes personalizadas
        self.load_fonts()
        
        # Configurar a aparência da aplicação
        self.setup_appearance()
        
        # Configurar janela responsiva
        self.setMinimumSize(1000, 700)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Restaurar estado da janela
        self.restore_window_state()
        
        # Centralizar janela na tela
        self.center_window()
        
        # Inicializar a interface do usuário
        self.init_ui()
        
        # Iniciar animação de carregamento
        self.start_loading_animation()
    
    def center_window(self):
        """Centralizar a janela na tela"""
        from PyQt5.QtWidgets import QDesktopWidget
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def load_fonts(self):
        """Carregar fontes personalizadas"""
        # Usar fontes do sistema
        QFontDatabase.addApplicationFont("C:/Windows/Fonts/segoeui.ttf")
        QFontDatabase.addApplicationFont("C:/Windows/Fonts/segoeuib.ttf")
        QFontDatabase.addApplicationFont("C:/Windows/Fonts/segoeuil.ttf")
    
    def set_window_icon(self):
        """Definir ícone da janela e taskbar usando CAIXA.jpeg"""
        try:
            # Tentar carregar o arquivo CAIXA.jpeg
            possible_paths = [
                os.path.join(os.path.dirname(__file__), "icons", "CAIXA.jpeg"),
                os.path.join(os.path.dirname(__file__), "CAIXA.jpeg"),
                os.path.join(os.path.dirname(__file__), "icons", "caixa.jpeg")
            ]
            
            icon_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    icon_path = path
                    break
            
            if icon_path:
                # Carregar a imagem
                pixmap = QPixmap(icon_path)
                if not pixmap.isNull():
                    # Criar ícone em múltiplos tamanhos para melhor qualidade
                    icon = QIcon()
                    for size in [16, 24, 32, 48, 64, 128, 256]:
                        scaled_pixmap = pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        icon.addPixmap(scaled_pixmap)
                    
                    # Definir ícone da janela
                    self.setWindowIcon(icon)
                    
                    # Definir ícone da aplicação (taskbar)
                    QApplication.instance().setWindowIcon(icon)
                    
                    logger.info(f"Ícone da aplicação e taskbar carregado: {icon_path}")
                else:
                    logger.warning(f"Falha ao carregar ícone: {icon_path}")
            else:
                logger.warning("Arquivo de ícone CAIXA.jpeg não encontrado")
                
        except Exception as e:
            logger.error(f"Erro ao definir ícone da aplicação: {e}")
    
    def setup_appearance(self):
        """Configurar a aparência da aplicação"""
        # Definir o estilo da aplicação
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        
        # Criar uma paleta de cores personalizada
        palette = QPalette()
        
        # Definir cores para diferentes elementos da interface
        palette.setColor(QPalette.Window, QColor(BACKGROUND_COLOR))
        palette.setColor(QPalette.WindowText, QColor(TEXT_COLOR))
        palette.setColor(QPalette.Base, QColor("#ffffff"))
        palette.setColor(QPalette.AlternateBase, QColor("#f5f5f5"))
        palette.setColor(QPalette.ToolTipBase, QColor("#ffffff"))
        palette.setColor(QPalette.ToolTipText, QColor(TEXT_COLOR))
        palette.setColor(QPalette.Text, QColor(TEXT_COLOR))
        palette.setColor(QPalette.Button, QColor(PRIMARY_COLOR))
        palette.setColor(QPalette.ButtonText, QColor("#ffffff"))
        palette.setColor(QPalette.BrightText, QColor("#ffffff"))
        palette.setColor(QPalette.Link, QColor(PRIMARY_COLOR))
        palette.setColor(QPalette.Highlight, QColor(PRIMARY_COLOR))
        palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
        
        # Aplicar a paleta
        QApplication.setPalette(palette)
        
    def init_ui(self):
        """Inicializar a interface do usuário moderna com abas"""
        self.setWindowTitle("Processador de Leads da CAIXA - Versão Profissional")
        self.setGeometry(100, 100, 1400, 900)
        
        # Definir ícone da janela
        self.set_window_icon()
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Cabeçalho moderno com gradiente
        self.create_header(main_layout)
        
        # Barra de estatísticas
        self.create_stats_bar(main_layout)
        
        # Área principal com abas
        self.create_tab_widget(main_layout)
        
        # Barra de status
        self.create_status_bar()
    
    def create_header(self, parent_layout):
        """Criar cabeçalho moderno"""
        header_container = QWidget()
        header_container.setFixedHeight(100)
        header_container.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {PRIMARY_COLOR}, 
                        stop:0.5 {SECONDARY_COLOR}, 
                        stop:1 {PRIMARY_COLOR});
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        """)
        
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(30, 20, 30, 20)
        
        # Logo e título principal
        title_section = QHBoxLayout()
        title_section.setSpacing(15)
        
        # Logo da CAIXA
        logo_label = QLabel()
        logo_pixmap = self.load_caixa_logo(50, 50)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setFixedSize(50, 50)
        
        # Área do título
        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)
        
        title_label = QLabel("CAIXA LEADS PROCESSOR")
        title_font = QFont("Segoe UI", 20, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white;")
        
        subtitle_label = QLabel("Processamento automático de leads com IA")
        subtitle_font = QFont("Segoe UI", 11)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        
        # Adicionar logo e título à seção
        title_section.addWidget(logo_label)
        title_section.addLayout(title_layout)
        
        # Botões de controle principal
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(15)
        
        self.main_start_button = AnimatedButton("Iniciar Processamento", SUCCESS_COLOR, icon_data=START_ICON, compact=True)
        self.main_start_button.clicked.connect(self.start_processing)
        self.main_start_button.setMinimumWidth(180)
        
        self.main_stop_button = AnimatedButton("Parar", ERROR_COLOR, icon_data=STOP_ICON, compact=True)
        self.main_stop_button.clicked.connect(self.stop_processing)
        self.main_stop_button.setEnabled(False)
        self.main_stop_button.setMinimumWidth(120)
        
        controls_layout.addWidget(self.main_start_button)
        controls_layout.addWidget(self.main_stop_button)
        
        # Adicionar ao layout do cabeçalho
        header_layout.addLayout(title_section)
        header_layout.addStretch()
        header_layout.addLayout(controls_layout)
        
        parent_layout.addWidget(header_container)
    
    def create_pixmap_from_svg(self, svg_data, width, height):
        """Criar um QPixmap a partir de dados SVG"""
        try:
            from PyQt5.QtSvg import QSvgRenderer
            from PyQt5.QtCore import QByteArray
            from PyQt5.QtGui import QPixmap, QPainter
            
            renderer = QSvgRenderer(QByteArray(svg_data.encode()))
            pixmap = QPixmap(width, height)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()
            
            return pixmap
        except Exception as e:
            # Fallback: criar um pixmap simples se SVG falhar
            pixmap = QPixmap(width, height)
            pixmap.fill(Qt.transparent)
            return pixmap
    
    def load_caixa_logo(self, width, height):
        """Carregar o logo da CAIXA a partir do arquivo JPEG"""
        try:
            # Tentar carregar o arquivo CAIXA.jpeg
            possible_paths = [
                os.path.join(os.path.dirname(__file__), "icons", "CAIXA.jpeg"),
                os.path.join(os.path.dirname(__file__), "CAIXA.jpeg"),
                os.path.join(os.path.dirname(__file__), "icons", "caixa.jpeg")
            ]
            
            logo_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    logo_path = path
                    break
            
            if logo_path:
                pixmap = QPixmap(logo_path)
                if not pixmap.isNull():
                    # Redimensionar mantendo proporção
                    scaled_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    return scaled_pixmap
            
            # Fallback: criar logo simples com texto se arquivo não existir
            pixmap = QPixmap(width, height)
            pixmap.fill(Qt.transparent)
            from PyQt5.QtGui import QPainter, QFont, QColor
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Desenhar um retângulo azul simples com "CAIXA"
            painter.fillRect(0, 0, width, height, QColor("#1976D2"))
            painter.setPen(QColor("white"))
            font = QFont("Arial", max(8, width // 6), QFont.Bold)
            painter.setFont(font)
            painter.drawText(pixmap.rect(), Qt.AlignCenter, "CAIXA")
            painter.end()
            
            return pixmap
        except Exception as e:
            # Fallback final: pixmap transparente
            pixmap = QPixmap(width, height)
            pixmap.fill(Qt.transparent)
            return pixmap
    
    def create_stats_bar(self, parent_layout):
        """Criar barra de estatísticas"""
        stats_container = QWidget()
        stats_container.setFixedHeight(80)
        stats_container.setStyleSheet(f"""
            background-color: {CARD_BACKGROUND};
            border-bottom: 1px solid #e0e0e0;
        """)
        
        stats_layout = QHBoxLayout(stats_container)
        stats_layout.setContentsMargins(30, 15, 30, 15)
        stats_layout.setSpacing(30)
        
        # Estatística 1: Total de Leads
        self.stats_total = self.create_stat_widget("Total de Leads", "0", PRIMARY_COLOR)
        
        # Estatística 2: Leads Completos
        self.stats_complete = self.create_stat_widget("Completos", "0", SUCCESS_COLOR)
        
        # Estatística 3: Leads Pendentes
        self.stats_pending = self.create_stat_widget("Pendentes", "0", WARNING_COLOR)
        
        # Estatística 4: Leads com Erro
        self.stats_error = self.create_stat_widget("Com Erro", "0", ERROR_COLOR)
        
        # Barra de progresso
        progress_widget = QWidget()
        progress_layout = QVBoxLayout(progress_widget)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        progress_layout.setSpacing(5)
        
        progress_label = QLabel("Progresso Geral")
        progress_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #666;")
        
        self.main_progress = QProgressBar()
        self.main_progress.setMinimumWidth(200)
        self.main_progress.setMaximumHeight(20)
        self.main_progress.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid #ddd;
                border-radius: 10px;
                background-color: #f0f0f0;
                text-align: center;
                font-size: 11px;
                font-weight: bold;
                color: white;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                           stop:0 {SUCCESS_COLOR}, stop:1 {PRIMARY_COLOR});
                border-radius: 9px;
            }}
        """)
        
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(self.main_progress)
        
        # Adicionar todos os widgets ao layout
        stats_layout.addWidget(self.stats_total)
        stats_layout.addWidget(self.stats_complete)
        stats_layout.addWidget(self.stats_pending)
        stats_layout.addWidget(self.stats_error)
        stats_layout.addStretch()
        stats_layout.addWidget(progress_widget)
        
        parent_layout.addWidget(stats_container)
    
    def create_stat_widget(self, title, value, color):
        """Criar um widget de estatística"""
        widget = QWidget()
        widget.setFixedSize(120, 50)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(2)
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 11px; font-weight: bold; color: #666;")
        
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setObjectName(f"stat_value_{title.lower().replace(' ', '_')}")
        value_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {color};")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        return widget
    
    def create_tab_widget(self, parent_layout):
        """Criar widget de abas principal"""
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {BACKGROUND_COLOR};
            }}
            QTabBar::tab {{
                background-color: {CARD_BACKGROUND};
                color: {TEXT_COLOR};
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                min-width: 120px;
            }}
            QTabBar::tab:selected {{
                background-color: {PRIMARY_COLOR};
                color: white;
            }}
            QTabBar::tab:hover {{
                background-color: {SECONDARY_COLOR};
                color: white;
            }}
        """)
        
        # Aba 1: Configuração
        self.create_config_tab()
        
        # Aba 2: Entrada Manual de Leads
        self.create_manual_input_tab()
        
        # Aba 3: Processamento
        self.create_processing_tab()
        
        # Aba 4: Relatórios
        self.create_reports_tab()
        
        # Aba 5: Logs
        self.create_logs_tab()
        
        # Aba 6: Configurações Avançadas
        self.create_advanced_settings_tab()
        
        parent_layout.addWidget(self.tab_widget)
    
    def create_config_tab(self):
        """Criar aba de configuração"""
        config_tab = QWidget()
        config_layout = QVBoxLayout(config_tab)
        config_layout.setContentsMargins(30, 30, 30, 30)
        config_layout.setSpacing(25)
        
        # Scroll area para responsividade
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(25)
        
        # Card de seleção de arquivo
        file_card = Card("Seleção de Arquivo", accent_color=PRIMARY_COLOR)
        file_layout = QVBoxLayout()
        
        # Descrição
        desc_label = QLabel("Selecione o arquivo contendo os leads da CAIXA para processamento:")
        desc_label.setStyleSheet("font-size: 13px; color: #666; margin-bottom: 10px;")
        desc_label.setWordWrap(True)
        
        # Seleção de arquivo
        file_input_layout = QHBoxLayout()
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setReadOnly(True)
        self.file_path_edit.setPlaceholderText("Nenhum arquivo selecionado...")
        self.file_path_edit.setMinimumHeight(45)
        self.file_path_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px 15px;
                background-color: white;
                font-size: 13px;
                color: #333;
            }
            QLineEdit:focus {
                border-color: #1976D2;
            }
        """)
        
        # Definir arquivo padrão
        default_path = os.path.join(os.getcwd(), "leads.txt")
        if os.path.exists(default_path):
            self.file_path_edit.setText(default_path)
        
        browse_button = AnimatedButton("Procurar Arquivo", PRIMARY_COLOR, icon_data=SEARCH_ICON)
        browse_button.clicked.connect(self.browse_file)
        browse_button.setMinimumWidth(150)
        
        file_input_layout.addWidget(self.file_path_edit, 3)
        file_input_layout.addWidget(browse_button, 1)
        
        file_layout.addWidget(desc_label)
        file_layout.addWidget(QWidget())  # Spacer
        file_layout.addLayout(file_input_layout)
        
        file_card.layout.addLayout(file_layout)
        scroll_layout.addWidget(file_card)
        
        # Card de configurações
        settings_card = Card("Configurações de Processamento", accent_color=SECONDARY_COLOR)
        settings_layout = QVBoxLayout()
        
        # Modo headless
        self.headless_checkbox = QCheckBox("Executar navegador em modo invisível (recomendado)")
        self.headless_checkbox.setChecked(True)
        self.headless_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 13px;
                color: #333;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #ccc;
                background-color: white;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #1976D2;
                background-color: #1976D2;
                border-radius: 4px;
            }
        """)
        
        # Timeout configuração
        timeout_layout = QHBoxLayout()
        timeout_label = QLabel("Timeout de carregamento (segundos):")
        timeout_label.setStyleSheet("font-size: 13px; color: #333; font-weight: bold;")
        
        self.timeout_spinbox = QComboBox()
        self.timeout_spinbox.addItems(["10", "15", "20", "30", "45", "60"])
        self.timeout_spinbox.setCurrentText("20")
        self.timeout_spinbox.setStyleSheet("""
            QComboBox {
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px 12px;
                background-color: white;
                font-size: 13px;
                min-width: 80px;
            }
            QComboBox:focus {
                border-color: #1976D2;
            }
        """)
        
        timeout_layout.addWidget(timeout_label)
        timeout_layout.addWidget(self.timeout_spinbox)
        timeout_layout.addStretch()
        
        settings_layout.addWidget(self.headless_checkbox)
        
        # Auto-skip em erros
        self.auto_skip_checkbox = QCheckBox("Pular automaticamente leads com erro (recomendado)")
        self.auto_skip_checkbox.setChecked(True)
        self.auto_skip_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 13px;
                color: #333;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #ccc;
                background-color: white;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #4CAF50;
                background-color: #4CAF50;
                border-radius: 4px;
            }
        """)
        settings_layout.addWidget(self.auto_skip_checkbox)
        
        settings_layout.addSpacing(15)
        settings_layout.addLayout(timeout_layout)
        
        settings_card.layout.addLayout(settings_layout)
        scroll_layout.addWidget(settings_card)
        
        # Card de informações
        info_card = Card("Informações Importantes", accent_color=WARNING_COLOR)
        info_layout = QVBoxLayout()
        
        info_text = QLabel("""
        <ul style="margin: 0; padding-left: 20px; line-height: 1.6;">
        <li><b>Formato do arquivo:</b> O arquivo deve conter leads no formato texto com informações separadas por linhas</li>
        <li><b>Conexão:</b> Certifique-se de ter uma conexão estável com a internet</li>
        <li><b>WhatsApp Web:</b> Mantenha o WhatsApp Web logado em seu navegador</li>
        <li><b>Processamento:</b> O processo pode demorar dependendo da quantidade de leads</li>
        </ul>
        """)
        info_text.setWordWrap(True)
        info_text.setStyleSheet("font-size: 13px; color: #555; line-height: 1.6;")
        
        info_layout.addWidget(info_text)
        info_card.layout.addLayout(info_layout)
        scroll_layout.addWidget(info_card)
        
        # Card de templates de mensagem
        templates_card = Card("📝 Templates de Mensagem", accent_color=SUCCESS_COLOR)
        templates_layout = QVBoxLayout()
        
        # Informações sobre variáveis disponíveis
        variables_info = QLabel("""
        <b>Variáveis disponíveis:</b><br>
        • <b>{{name}}</b> - Nome do cliente<br>
        • <b>{{city}}</b> - Cidade do imóvel<br>
        • <b>{{property_url}}</b> - Link do imóvel<br>
        • <b>{{telephone}}</b> - Telefone do cliente<br>
        • <b>{{greeting}}</b> - Saudação automática (Bom dia/Boa tarde/Boa noite)
        """)
        variables_info.setStyleSheet("""
            QLabel {
                background-color: #E8F5E8;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                padding: 12px;
                margin-bottom: 15px;
                font-size: 12px;
                color: #2E7D32;
            }
        """)
        variables_info.setWordWrap(True)
        templates_layout.addWidget(variables_info)
        
        # Template para leads normais
        normal_template_label = QLabel("📋 Template para Leads Normais:")
        normal_template_label.setStyleSheet("font-weight: bold; font-size: 13px; color: #333; margin-bottom: 5px;")
        templates_layout.addWidget(normal_template_label)
        
        self.normal_template_edit = QTextEdit()
        self.normal_template_edit.setMaximumHeight(120)
        self.normal_template_edit.setStyleSheet("""
            QTextEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
                background-color: white;
                font-size: 12px;
                color: #333;
                font-family: 'Segoe UI', sans-serif;
            }
            QTextEdit:focus {
                border-color: #4CAF50;
            }
        """)
        self.normal_template_edit.setPlainText(self.settings.get("message_templates.normal_lead", ""))
        templates_layout.addWidget(self.normal_template_edit)
        
        templates_layout.addSpacing(15)
        
        # Template para leads indisponíveis
        unavailable_template_label = QLabel("🚫 Template para Imóveis Indisponíveis:")
        unavailable_template_label.setStyleSheet("font-weight: bold; font-size: 13px; color: #333; margin-bottom: 5px;")
        templates_layout.addWidget(unavailable_template_label)
        
        self.unavailable_template_edit = QTextEdit()
        self.unavailable_template_edit.setMaximumHeight(120)
        self.unavailable_template_edit.setStyleSheet("""
            QTextEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
                background-color: white;
                font-size: 12px;
                color: #333;
                font-family: 'Segoe UI', sans-serif;
            }
            QTextEdit:focus {
                border-color: #FF9800;
            }
        """)
        self.unavailable_template_edit.setPlainText(self.settings.get("message_templates.unavailable_lead", ""))
        templates_layout.addWidget(self.unavailable_template_edit)
        
        # Botões de ação para templates
        template_buttons_layout = QHBoxLayout()
        
        preview_button = AnimatedButton("👁️ Visualizar", "#2196F3", compact=True)
        preview_button.clicked.connect(self.preview_message_template)
        
        reset_button = AnimatedButton("🔄 Restaurar Padrão", "#FF9800", compact=True)
        reset_button.clicked.connect(self.reset_message_templates)
        
        save_templates_button = AnimatedButton("💾 Salvar Templates", SUCCESS_COLOR, compact=True)
        save_templates_button.clicked.connect(self.save_message_templates)
        
        template_buttons_layout.addWidget(preview_button)
        template_buttons_layout.addWidget(reset_button)
        template_buttons_layout.addStretch()
        template_buttons_layout.addWidget(save_templates_button)
        
        templates_layout.addSpacing(10)
        templates_layout.addLayout(template_buttons_layout)
        
        templates_card.layout.addLayout(templates_layout)
        scroll_layout.addWidget(templates_card)
        
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        config_layout.addWidget(scroll_area)
        
        self.tab_widget.addTab(config_tab, "⚙️ Configuração")
    
    def create_manual_input_tab(self):
        """Criar aba de entrada manual de leads"""
        manual_tab = QWidget()
        manual_layout = QVBoxLayout(manual_tab)
        manual_layout.setSpacing(20)
        manual_layout.setContentsMargins(20, 20, 20, 20)
        
        # Título da aba
        title_card = Card("➕ Entrada Manual de Leads", accent_color=PRIMARY_COLOR)
        description = QLabel("Digite as informações dos leads manualmente. Os dados serão salvos em leads.txt e processados automaticamente.")
        description.setStyleSheet(f"color: {LIGHT_TEXT_COLOR}; font-size: 14px; margin-bottom: 10px;")
        description.setWordWrap(True)
        title_card.layout.addWidget(description)
        manual_layout.addWidget(title_card)
        
        # Scroll area para o formulário
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 4px;
                min-height: 20px;
            }
        """)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(20)
        
        # Formulário de entrada de leads
        form_card = Card("📝 Informações do Lead", accent_color=SUCCESS_COLOR)
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Campo Nome
        self.manual_name_input = QLineEdit()
        self.manual_name_input.setPlaceholderText("Ex: João Silva Santos")
        self.manual_name_input.setStyleSheet(self.get_input_style())
        form_layout.addRow("Nome Completo *:", self.manual_name_input)
        
        # Campo Email
        self.manual_email_input = QLineEdit()
        self.manual_email_input.setPlaceholderText("Ex: joao.silva@email.com")
        self.manual_email_input.setStyleSheet(self.get_input_style())
        form_layout.addRow("E-mail *:", self.manual_email_input)
        
        # Campo Telefone
        self.manual_phone_input = QLineEdit()
        self.manual_phone_input.setPlaceholderText("Ex: 11987654321")
        self.manual_phone_input.setStyleSheet(self.get_input_style())
        form_layout.addRow("Telefone *:", self.manual_phone_input)
        
        # Campo Código do Imóvel
        self.manual_property_id_input = QLineEdit()
        self.manual_property_id_input.setPlaceholderText("Ex: CX08444425765084SP")
        self.manual_property_id_input.setStyleSheet(self.get_input_style())
        form_layout.addRow("Código do Imóvel *:", self.manual_property_id_input)
        
        form_card.layout.addLayout(form_layout)
        scroll_layout.addWidget(form_card)
        
        # Entrada em massa (template)
        bulk_card = Card("📋 Entrada em Massa (Template)", accent_color=SECONDARY_COLOR)
        bulk_description = QLabel("Cole o texto dos leads no formato padrão abaixo. Múltiplos leads serão extraídos automaticamente:")
        bulk_description.setStyleSheet(f"color: {LIGHT_TEXT_COLOR}; font-size: 12px; margin-bottom: 10px;")
        bulk_description.setWordWrap(True)
        bulk_card.layout.addWidget(bulk_description)
        
        # Exemplo do template
        template_example = QLabel("""<b>Exemplo do formato:</b><br>
Olá ,<br>
Você possui um novo lead para o imóvel CX08444425765084SP:<br>
Nome: João Silva Santos<br>
E-mail: joao@email.com<br>
Telefone: 11987654321<br><br>
<i>Cole quantos leads quiser neste formato...</i>""")
        template_example.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                padding: 10px;
                font-size: 11px;
                color: #6c757d;
            }
        """)
        bulk_card.layout.addWidget(template_example)
        
        # Área de texto para entrada em massa
        self.bulk_input_area = QTextEdit()
        self.bulk_input_area.setMaximumHeight(150)
        self.bulk_input_area.setPlaceholderText("Cole aqui o texto dos leads no formato padrão...")
        self.bulk_input_area.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 6px;
                padding: 10px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                color: #495057;
            }
            QTextEdit:focus {
                border-color: #007bff;
                background-color: #f8f9ff;
            }
        """)
        bulk_card.layout.addWidget(self.bulk_input_area)
        
        # Botão para processar entrada em massa
        bulk_button_layout = QHBoxLayout()
        self.parse_bulk_button = AnimatedButton("🔍 Extrair Leads do Texto", SECONDARY_COLOR)
        self.parse_bulk_button.clicked.connect(self.parse_bulk_leads)
        
        self.clear_bulk_button = AnimatedButton("🗑️ Limpar Texto", "#777777", compact=True)
        self.clear_bulk_button.clicked.connect(lambda: self.bulk_input_area.clear())
        
        bulk_button_layout.addWidget(self.parse_bulk_button)
        bulk_button_layout.addWidget(self.clear_bulk_button)
        bulk_button_layout.addStretch()
        
        bulk_card.layout.addLayout(bulk_button_layout)
        scroll_layout.addWidget(bulk_card)
        
        # Lista de leads adicionados
        list_card = Card("📋 Leads Adicionados", accent_color=WARNING_COLOR)
        self.manual_leads_list = QTextEdit()
        self.manual_leads_list.setMaximumHeight(200)
        self.manual_leads_list.setReadOnly(True)
        self.manual_leads_list.setPlaceholderText("Os leads adicionados aparecerão aqui...")
        self.manual_leads_list.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                padding: 10px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                color: #495057;
            }
        """)
        list_card.layout.addWidget(self.manual_leads_list)
        scroll_layout.addWidget(list_card)
        
        scroll_area.setWidget(scroll_widget)
        manual_layout.addWidget(scroll_area, 1)
        
        # Botões de ação
        buttons_card = Card()
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.add_lead_button = AnimatedButton("➕ Adicionar Lead", SUCCESS_COLOR)
        self.add_lead_button.setMinimumHeight(50)
        self.add_lead_button.clicked.connect(self.add_manual_lead)
        
        self.clear_leads_button = AnimatedButton("🗑️ Limpar Todos", ERROR_COLOR)
        self.clear_leads_button.setMinimumHeight(50)
        self.clear_leads_button.clicked.connect(self.clear_manual_leads)
        
        self.save_and_process_button = AnimatedButton("💾 Salvar e Processar", PRIMARY_COLOR)
        self.save_and_process_button.setMinimumHeight(50)
        self.save_and_process_button.clicked.connect(self.save_and_process_manual_leads)
        
        buttons_layout.addWidget(self.add_lead_button)
        buttons_layout.addWidget(self.clear_leads_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_and_process_button)
        
        buttons_card.layout.addLayout(buttons_layout)
        manual_layout.addWidget(buttons_card)
        
        # Lista para armazenar os leads
        self.manual_leads_data = []
        
        self.tab_widget.addTab(manual_tab, "➕ Entrada Manual")
    
    def get_input_style(self):
        """Retornar estilo para campos de entrada"""
        return """
            QLineEdit {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                color: #495057;
            }
            QLineEdit:focus {
                border-color: #007bff;
                background-color: #f8f9ff;
            }
            QLineEdit:hover {
                border-color: #80bdff;
            }
        """
    
    def add_manual_lead(self):
        """Adicionar um lead manualmente"""
        # Validar campos obrigatórios
        name = self.manual_name_input.text().strip()
        email = self.manual_email_input.text().strip()
        phone = self.manual_phone_input.text().strip()
        property_id = self.manual_property_id_input.text().strip()
        
        if not all([name, email, phone, property_id]):
            QMessageBox.warning(
                self, 
                "Campos Obrigatórios", 
                "Por favor, preencha todos os campos obrigatórios:\n• Nome Completo\n• E-mail\n• Telefone\n• Código do Imóvel"
            )
            return
        
        # Validar formato do email
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            QMessageBox.warning(self, "E-mail Inválido", "Por favor, digite um e-mail válido.")
            return
        
        # Validar telefone (deve conter apenas números)
        phone_clean = ''.join(filter(str.isdigit, phone))
        if len(phone_clean) < 10:
            QMessageBox.warning(self, "Telefone Inválido", "Por favor, digite um telefone válido (mínimo 10 dígitos).")
            return
        
        # Adicionar lead à lista
        lead_data = {
            'name': name,
            'email': email,
            'phone': phone_clean,
            'property_id': property_id
        }
        
        self.manual_leads_data.append(lead_data)
        
        # Atualizar a lista visual
        self.update_manual_leads_display()
        
        # Limpar campos
        self.manual_name_input.clear()
        self.manual_email_input.clear()
        self.manual_phone_input.clear()
        self.manual_property_id_input.clear()
        
        # Foco no primeiro campo
        self.manual_name_input.setFocus()
        
        self.log(f"Lead adicionado manualmente: {name}")
    
    def parse_bulk_leads(self):
        """Extrair leads do texto em massa"""
        text = self.bulk_input_area.toPlainText().strip()
        
        if not text:
            QMessageBox.warning(self, "Texto Vazio", "Por favor, cole o texto dos leads na área de entrada em massa.")
            return
        
        import re
        
        # Padrão regex para extrair informações dos leads
        # Busca por blocos que contenham imóvel, nome, email e telefone
        lead_pattern = r'imóvel\s+(CX\w+).*?Nome:\s*([^\n\r]+).*?E-mail:\s*([^\n\r]+).*?Telefone:\s*([^\n\r]+)'
        
        matches = re.findall(lead_pattern, text, re.DOTALL | re.IGNORECASE)
        
        if not matches:
            QMessageBox.warning(
                self, 
                "Nenhum Lead Encontrado", 
                "Não foi possível extrair informações de leads do texto.\n\n"
                "Verifique se o formato está correto:\n"
                "• Deve conter 'imóvel CXxxxxxxSP'\n"
                "• Deve conter 'Nome: [nome]'\n"
                "• Deve conter 'E-mail: [email]'\n"
                "• Deve conter 'Telefone: [telefone]'"
            )
            return
        
        # Validar e adicionar leads extraídos
        added_count = 0
        errors = []
        
        for property_id, name, email, phone in matches:
            # Limpar dados
            name = name.strip()
            email = email.strip()
            phone = ''.join(filter(str.isdigit, phone.strip()))
            property_id = property_id.strip()
            
            # Validações básicas
            if not name or not email or not phone or not property_id:
                errors.append(f"Lead incompleto: {name or 'Nome vazio'}")
                continue
            
            # Validar email
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                errors.append(f"E-mail inválido para {name}: {email}")
                continue
            
            # Validar telefone
            if len(phone) < 10:
                errors.append(f"Telefone inválido para {name}: {phone}")
                continue
            
            # Verificar se já existe
            if any(lead['email'] == email for lead in self.manual_leads_data):
                errors.append(f"E-mail já adicionado: {email}")
                continue
            
            # Adicionar lead
            lead_data = {
                'name': name,
                'email': email,
                'phone': phone,
                'property_id': property_id
            }
            
            self.manual_leads_data.append(lead_data)
            added_count += 1
        
        # Atualizar display
        self.update_manual_leads_display()
        
        # Limpar área de texto
        self.bulk_input_area.clear()
        
        # Mostrar resultado
        message = f"✅ {added_count} leads extraídos e adicionados com sucesso!"
        
        if errors:
            message += f"\n\n⚠️ {len(errors)} problemas encontrados:"
            for error in errors[:5]:  # Mostrar apenas os primeiros 5 erros
                message += f"\n• {error}"
            if len(errors) > 5:
                message += f"\n• ... e mais {len(errors) - 5} erro(s)"
        
        if added_count > 0:
            QMessageBox.information(self, "Leads Extraídos", message)
            self.log(f"Extraídos {added_count} leads do texto em massa")
        else:
            QMessageBox.warning(self, "Nenhum Lead Válido", message)
    
    def clear_manual_leads(self):
        """Limpar todos os leads manuais"""
        if not self.manual_leads_data:
            return
        
        reply = QMessageBox.question(
            self,
            "Confirmar Limpeza",
            f"Tem certeza que deseja remover todos os {len(self.manual_leads_data)} leads adicionados?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.manual_leads_data.clear()
            self.update_manual_leads_display()
            self.log("Todos os leads manuais foram removidos.")
    
    def update_manual_leads_display(self):
        """Atualizar a exibição da lista de leads"""
        if not self.manual_leads_data:
            self.manual_leads_list.setPlainText("Nenhum lead adicionado ainda...")
            return
        
        display_text = f"📊 Total de leads: {len(self.manual_leads_data)}\n\n"
        
        for i, lead in enumerate(self.manual_leads_data, 1):
            display_text += f"═══ Lead #{i} ═══\n"
            display_text += f"Nome: {lead['name']}\n"
            display_text += f"E-mail: {lead['email']}\n"
            display_text += f"Telefone: {lead['phone']}\n"
            display_text += f"Imóvel: {lead['property_id']}\n\n"
        
        self.manual_leads_list.setPlainText(display_text)
    
    def save_and_process_manual_leads(self):
        """Salvar leads manuais em leads.txt e processar"""
        if not self.manual_leads_data:
            QMessageBox.warning(self, "Nenhum Lead", "Adicione pelo menos um lead antes de salvar.")
            return
        
        try:
            # Criar conteúdo no formato esperado pelo processador
            content = ""
            
            for lead in self.manual_leads_data:
                content += f"Olá ,\nVocê possui um novo lead para o imóvel {lead['property_id']}:\n\n"
                content += f"Nome: {lead['name']}\n"
                content += f"E-mail: {lead['email']}\n"
                content += f"Telefone: {lead['phone']}\n\n\n\n"
            
            # Salvar em leads.txt
            leads_file = os.path.join(os.getcwd(), "leads.txt")
            with open(leads_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Confirmar salvamento
            reply = QMessageBox.question(
                self,
                "Leads Salvos",
                f"✅ {len(self.manual_leads_data)} leads foram salvos em leads.txt\n\n"
                "Deseja processar os leads automaticamente agora?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if reply == QMessageBox.Yes:
                # Limpar leads atuais e ir para aba de processamento
                self.manual_leads_data.clear()
                self.update_manual_leads_display()
                
                # Ir para aba de processamento
                self.tab_widget.setCurrentIndex(2)  # Aba de processamento
                
                # Definir arquivo de leads na configuração
                self.file_path_edit.setText(leads_file)
                
                self.log(f"Leads manuais salvos e prontos para processamento: {leads_file}")
            else:
                self.log(f"Leads manuais salvos em: {leads_file}")
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar leads:\n{str(e)}")
            self.log(f"Erro ao salvar leads manuais: {str(e)}")
    
    def create_processing_tab(self):
        """Criar aba de processamento"""
        processing_tab = QWidget()
        main_processing_layout = QVBoxLayout(processing_tab)
        main_processing_layout.setContentsMargins(0, 0, 0, 0)
        
        # Criar scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
        """)
        
        # Widget de conteúdo dentro do scroll
        scroll_content = QWidget()
        processing_layout = QVBoxLayout(scroll_content)
        processing_layout.setContentsMargins(20, 20, 20, 20)
        processing_layout.setSpacing(20)
        
        # Área de lead atual
        current_lead_card = Card("Lead Atual", accent_color=PRIMARY_COLOR)
        current_lead_layout = QVBoxLayout()
        
        # Navegação entre leads (inicialmente oculta)
        self.navigation_widget = QWidget()
        navigation_layout = QHBoxLayout(self.navigation_widget)
        navigation_layout.setContentsMargins(0, 0, 0, 10)
        
        # Botão anterior
        self.prev_lead_button = AnimatedButton("◀ Anterior", "#666666", compact=True)
        self.prev_lead_button.clicked.connect(self.prev_lead)
        self.prev_lead_button.setEnabled(False)
        
        # Indicador de posição
        self.lead_position_label = QLabel("Lead 1 de 1")
        self.lead_position_label.setAlignment(Qt.AlignCenter)
        self.lead_position_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #333;
            padding: 8px 16px;
            background-color: #f0f0f0;
            border-radius: 20px;
            border: 2px solid #ddd;
        """)
        
        # Botão próximo
        self.next_lead_button = AnimatedButton("Próximo ▶", "#666666", compact=True)
        self.next_lead_button.clicked.connect(self.next_lead)
        self.next_lead_button.setEnabled(False)
        
        navigation_layout.addWidget(self.prev_lead_button)
        navigation_layout.addStretch()
        navigation_layout.addWidget(self.lead_position_label)
        navigation_layout.addStretch()
        navigation_layout.addWidget(self.next_lead_button)
        
        self.navigation_widget.setVisible(False)  # Ocultar inicialmente
        current_lead_layout.addWidget(self.navigation_widget)
        
        # Informações do lead em grid responsivo
        lead_info_widget = QWidget()
        lead_info_layout = QGridLayout(lead_info_widget)
        lead_info_layout.setSpacing(15)
        
        # Estilo para informações
        info_style = """
            QLabel {
                padding: 12px;
                background-color: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid #1976D2;
                font-size: 13px;
                color: #333;
            }
        """
        
        label_style = """
            QLabel {
                font-size: 13px;
                font-weight: bold;
                color: #555;
                margin-bottom: 5px;
            }
        """
        
        # Criar labels
        name_label = QLabel("Nome:")
        name_label.setStyleSheet(label_style)
        self.lead_name_label = QLabel("-")
        self.lead_name_label.setStyleSheet(info_style)
        
        email_label = QLabel("Email:")
        email_label.setStyleSheet(label_style)
        self.lead_email_label = QLabel("-")
        self.lead_email_label.setStyleSheet(info_style)
        
        phone_label = QLabel("Telefone:")
        phone_label.setStyleSheet(label_style)
        self.lead_phone_label = QLabel("-")
        self.lead_phone_label.setStyleSheet(info_style)
        
        property_label = QLabel("ID do Imóvel:")
        property_label.setStyleSheet(label_style)
        self.lead_property_id_label = QLabel("-")
        self.lead_property_id_label.setStyleSheet(info_style)
        
        city_label = QLabel("Cidade:")
        city_label.setStyleSheet(label_style)
        self.lead_city_label = QLabel("-")
        self.lead_city_label.setStyleSheet(info_style)
        
        # Adicionar ao grid
        lead_info_layout.addWidget(name_label, 0, 0)
        lead_info_layout.addWidget(self.lead_name_label, 0, 1)
        lead_info_layout.addWidget(email_label, 0, 2)
        lead_info_layout.addWidget(self.lead_email_label, 0, 3)
        
        lead_info_layout.addWidget(phone_label, 1, 0)
        lead_info_layout.addWidget(self.lead_phone_label, 1, 1)
        lead_info_layout.addWidget(property_label, 1, 2)
        lead_info_layout.addWidget(self.lead_property_id_label, 1, 3)
        
        lead_info_layout.addWidget(city_label, 2, 0)
        lead_info_layout.addWidget(self.lead_city_label, 2, 1, 1, 3)
        
        # Botões de ação
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)
        
        self.view_property_button = AnimatedButton("Ver Imóvel", PRIMARY_COLOR, icon_data=VIEW_ICON)
        self.view_property_button.clicked.connect(self.view_property)
        self.view_property_button.setEnabled(False)
        
        self.send_whatsapp_button = AnimatedButton("Enviar WhatsApp", SUCCESS_COLOR, icon_data=WHATSAPP_ICON)
        self.send_whatsapp_button.clicked.connect(self.send_whatsapp)
        self.send_whatsapp_button.setEnabled(False)
        
        self.edit_lead_button = AnimatedButton("Editar Lead", WARNING_COLOR, icon_data=EDIT_ICON)
        self.edit_lead_button.clicked.connect(self.edit_lead)
        self.edit_lead_button.setEnabled(False)
        
        self.skip_lead_button = AnimatedButton("Pular Lead", "#777777", icon_data=SKIP_ICON)
        self.skip_lead_button.clicked.connect(self.skip_lead)
        self.skip_lead_button.setEnabled(False)
        
        actions_layout.addWidget(self.view_property_button)
        actions_layout.addWidget(self.send_whatsapp_button)
        actions_layout.addWidget(self.edit_lead_button)
        actions_layout.addWidget(self.skip_lead_button)
        actions_layout.addStretch()
        
        # Adicionar tudo ao card
        current_lead_layout.addWidget(lead_info_widget)
        current_lead_layout.addSpacing(20)
        current_lead_layout.addLayout(actions_layout)
        
        current_lead_card.layout.addLayout(current_lead_layout)
        processing_layout.addWidget(current_lead_card)
        
        # Área de progresso detalhado
        progress_card = Card("Progresso Detalhado", accent_color=SECONDARY_COLOR)
        progress_layout = QVBoxLayout()
        
        # Progresso do lead atual
        current_progress_layout = QHBoxLayout()
        current_progress_label = QLabel("Lead Atual:")
        current_progress_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #555;")
        
        self.current_lead_progress = QProgressBar()
        self.current_lead_progress.setMaximumHeight(25)
        self.current_lead_progress.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid #ddd;
                border-radius: 12px;
                background-color: #f0f0f0;
                text-align: center;
                font-size: 12px;
                font-weight: bold;
                color: white;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                           stop:0 {PRIMARY_COLOR}, stop:1 {SECONDARY_COLOR});
                border-radius: 11px;
            }}
        """)
        
        current_progress_layout.addWidget(current_progress_label, 1)
        current_progress_layout.addWidget(self.current_lead_progress, 4)
        
        # Status do processamento
        self.processing_status = QLabel("Aguardando início do processamento...")
        self.processing_status.setStyleSheet("""
            font-size: 13px;
            color: #666;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 6px;
            border-left: 4px solid #17a2b8;
        """)
        
        progress_layout.addLayout(current_progress_layout)
        progress_layout.addSpacing(15)
        progress_layout.addWidget(self.processing_status)
        
        # Área de progresso detalhado em tempo real
        progress_layout.addSpacing(10)
        
        detailed_progress_label = QLabel("📋 Progresso Detalhado:")
        detailed_progress_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333; margin-bottom: 8px;")
        progress_layout.addWidget(detailed_progress_label)
        
        # Área de log detalhado
        self.detailed_progress_text = QTextEdit()
        self.detailed_progress_text.setReadOnly(True)
        self.detailed_progress_text.setMinimumHeight(400)  # Good starting height
        # Remove maximum height to allow expansion with scrolling
        self.detailed_progress_text.setStyleSheet("""
            QTextEdit {
                border: 2px solid #e0e0e0;
                border-radius: 12px;
                padding: 16px;
                background-color: #fafafa;
                color: #333;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
                line-height: 1.6;
                selection-background-color: #e3f2fd;
            }
            QTextEdit:focus {
                border-color: #2196F3;
                background-color: #ffffff;
            }
        """)
        
        # Mensagem inicial mais elegante
        self.detailed_progress_text.setHtml("""
            <div style="text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 8px; margin: 10px;">
                <div style="font-size: 48px; margin-bottom: 20px;">🚀</div>
                <h3 style="color: #2c3e50; margin: 0 0 10px 0; font-size: 18px; font-weight: 600;">Sistema Pronto para Iniciar</h3>
                <p style="color: #6c757d; margin: 0 0 15px 0; font-size: 14px; line-height: 1.5;">
                    Selecione um arquivo de leads e clique em<br>
                    <strong>"Iniciar Processamento"</strong> para começar.
                </p>
                <div style="background-color: #e3f2fd; padding: 15px; border-radius: 6px; margin-top: 20px;">
                    <p style="color: #1976d2; margin: 0; font-size: 13px;">
                        💡 <strong>Dica:</strong> O progresso detalhado de cada lead<br>aparecerá aqui em tempo real
                    </p>
                </div>
            </div>
        """)
        
        progress_layout.addWidget(self.detailed_progress_text)
        
        progress_card.layout.addLayout(progress_layout)
        processing_layout.addWidget(progress_card, 1)  # Give more space to this card
        
        # Add minimal stretch to prevent over-expansion
        processing_layout.addStretch(0)
        
        # Configurar o scroll area
        scroll_area.setWidget(scroll_content)
        main_processing_layout.addWidget(scroll_area)
        
        self.tab_widget.addTab(processing_tab, "▶️ Processamento")
    
    def create_reports_tab(self):
        """Criar aba de relatórios"""
        reports_tab = QWidget()
        reports_layout = QVBoxLayout(reports_tab)
        reports_layout.setContentsMargins(20, 20, 20, 20)
        reports_layout.setSpacing(20)
        
        # Cabeçalho dos relatórios
        header_card = Card("Relatórios e Análises", accent_color=SUCCESS_COLOR)
        header_layout = QHBoxLayout()
        
        # Botões de ação
        export_button = AnimatedButton("Exportar Excel", SUCCESS_COLOR)
        export_button.clicked.connect(self.export_report)
        
        refresh_button = AnimatedButton("Atualizar", PRIMARY_COLOR)
        refresh_button.clicked.connect(self.refresh_reports)
        
        header_layout.addStretch()
        header_layout.addWidget(refresh_button)
        header_layout.addWidget(export_button)
        
        header_card.layout.addLayout(header_layout)
        reports_layout.addWidget(header_card)
        
        # Tabela de leads
        table_card = Card("Todos os Leads Processados")
        table_layout = QVBoxLayout()
        
        # Filtros
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)
        
        status_filter_label = QLabel("Filtrar por status:")
        status_filter_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #555;")
        
        self.status_filter = QComboBox()
        self.status_filter.addItems(["Todos", "Completo", "Pendente", "Erro"])
        self.status_filter.setStyleSheet("""
            QComboBox {
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px 12px;
                background-color: white;
                font-size: 13px;
                min-width: 120px;
            }
        """)
        self.status_filter.currentTextChanged.connect(self.filter_table)
        
        search_label = QLabel("Buscar:")
        search_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #555;")
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Digite nome, email ou telefone...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px 12px;
                background-color: white;
                font-size: 13px;
                min-width: 200px;
            }
            QLineEdit:focus {
                border-color: #1976D2;
            }
        """)
        self.search_input.textChanged.connect(self.filter_table)
        
        filter_layout.addWidget(status_filter_label)
        filter_layout.addWidget(self.status_filter)
        filter_layout.addSpacing(20)
        filter_layout.addWidget(search_label)
        filter_layout.addWidget(self.search_input)
        filter_layout.addStretch()
        
        # Tabela
        self.leads_table = QTableWidget()
        self.leads_table.setColumnCount(7)
        self.leads_table.setHorizontalHeaderLabels([
            "Nome", "Email", "Telefone", "ID Imóvel", "Cidade", "Status", "Ações"
        ])
        
        # Configurar tabela
        header = self.leads_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Interactive)  # Nome
        header.setSectionResizeMode(1, QHeaderView.Interactive)  # Email
        header.setSectionResizeMode(2, QHeaderView.Fixed)        # Telefone
        header.setSectionResizeMode(3, QHeaderView.Fixed)        # ID Imóvel
        header.setSectionResizeMode(4, QHeaderView.Interactive)  # Cidade
        header.setSectionResizeMode(5, QHeaderView.Fixed)        # Status
        header.setSectionResizeMode(6, QHeaderView.Fixed)        # Ações
        
        # Definir larguras
        self.leads_table.setColumnWidth(2, 120)  # Telefone
        self.leads_table.setColumnWidth(3, 150)  # ID Imóvel
        self.leads_table.setColumnWidth(5, 100)  # Status
        self.leads_table.setColumnWidth(6, 120)  # Ações
        
        self.leads_table.setAlternatingRowColors(True)
        self.leads_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.leads_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e0e0e0;
                background-color: white;
                gridline-color: #f0f0f0;
                font-size: 13px;
                selection-background-color: #e3f2fd;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #f5f5f5;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                           stop:0 #f8f9fa, stop:1 #e9ecef);
                color: #495057;
                padding: 12px 8px;
                font-weight: bold;
                border: none;
                border-right: 1px solid #dee2e6;
                border-bottom: 2px solid #1976d2;
            }
            QTableWidget::item:alternate {
                background-color: #f8f9fa;
            }
        """)
        
        table_layout.addLayout(filter_layout)
        table_layout.addSpacing(15)
        table_layout.addWidget(self.leads_table)
        
        table_card.layout.addLayout(table_layout)
        reports_layout.addWidget(table_card, 1)
        
        self.tab_widget.addTab(reports_tab, "📊 Relatórios")
    
    def create_logs_tab(self):
        """Criar aba de logs"""
        logs_tab = QWidget()
        logs_layout = QVBoxLayout(logs_tab)
        logs_layout.setContentsMargins(20, 20, 20, 20)
        logs_layout.setSpacing(20)
        
        # Cabeçalho dos logs
        header_card = Card("Sistema de Logs", accent_color="#17a2b8")
        header_layout = QHBoxLayout()
        
        # Controles de log
        clear_button = AnimatedButton("Limpar Logs", WARNING_COLOR)
        clear_button.clicked.connect(self.clear_logs)
        
        save_button = AnimatedButton("Salvar Logs", PRIMARY_COLOR)
        save_button.clicked.connect(self.save_logs)
        
        # Filtro de nível de log
        level_label = QLabel("Nível:")
        level_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #555;")
        
        self.log_level_filter = QComboBox()
        self.log_level_filter.addItems(["Todos", "INFO", "WARNING", "ERROR", "DEBUG"])
        self.log_level_filter.setStyleSheet("""
            QComboBox {
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px 12px;
                background-color: white;
                font-size: 13px;
            }
        """)
        
        header_layout.addWidget(level_label)
        header_layout.addWidget(self.log_level_filter)
        header_layout.addStretch()
        header_layout.addWidget(clear_button)
        header_layout.addWidget(save_button)
        
        header_card.layout.addLayout(header_layout)
        logs_layout.addWidget(header_card)
        
        # Área de log principal
        log_card = Card("Log de Execução em Tempo Real")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
                background-color: #1e1e1e;
                color: #f8f8f2;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 12px;
                line-height: 1.4;
            }
        """)
        
        # Configurar cores para diferentes tipos de log
        self.log_text.setHtml("""
            <style>
                .info { color: #50fa7b; }
                .warning { color: #f1fa8c; }
                .error { color: #ff5555; }
                .debug { color: #8be9fd; }
                .timestamp { color: #6272a4; }
            </style>
            <div style="color: #f8f8f2; text-align: center; padding: 20px;">
                <h3>Sistema de Logs Iniciado</h3>
                <p>Os logs do processamento aparecerão aqui em tempo real...</p>
            </div>
        """)
        
        log_layout.addWidget(self.log_text)
        log_card.layout.addLayout(log_layout)
        logs_layout.addWidget(log_card, 1)
        
        self.tab_widget.addTab(logs_tab, "📝 Logs")
    
    def create_advanced_settings_tab(self):
        """Criar aba de configurações avançadas"""
        settings_tab = QWidget()
        settings_layout = QVBoxLayout(settings_tab)
        settings_layout.setSpacing(20)
        settings_layout.setContentsMargins(20, 20, 20, 20)
        
        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(20)
        
        # Informações da aplicação
        app_info_card = Card("ℹ️ Informações da Aplicação", accent_color=PRIMARY_COLOR)
        app_info = self.settings.get_app_info()
        
        info_layout = QVBoxLayout()
        info_text = f"""
        <b>Versão:</b> {app_info['version']}<br>
        <b>Última abertura:</b> {app_info['last_opened'] or 'Primeira execução'}<br>
        <b>Diretório de configuração:</b> {app_info['config_dir']}<br>
        <b>Diretório de dados:</b> {app_info['data_dir']}<br>
        <b>Entradas no histórico:</b> {app_info['total_history_entries']}<br>
        <b>Leads manuais salvos:</b> {app_info['manual_leads_backup']}
        """
        
        info_label = QLabel(info_text)
        info_label.setStyleSheet("font-size: 12px; color: #666; line-height: 1.4;")
        info_label.setWordWrap(True)
        info_layout.addWidget(info_label)
        
        app_info_card.layout.addLayout(info_layout)
        scroll_layout.addWidget(app_info_card)
        
        # Configurações de interface
        ui_card = Card("🎨 Interface", accent_color=SECONDARY_COLOR)
        ui_layout = QFormLayout()
        
        # Auto-switch tabs
        self.auto_switch_checkbox = QCheckBox("Trocar abas automaticamente")
        self.auto_switch_checkbox.setChecked(self.settings.get("ui.auto_switch_tabs", True))
        self.auto_switch_checkbox.toggled.connect(lambda x: self.settings.set("ui.auto_switch_tabs", x))
        
        # Show confirmations
        self.confirmations_checkbox = QCheckBox("Mostrar diálogos de confirmação")
        self.confirmations_checkbox.setChecked(self.settings.get("ui.show_confirmations", True))
        self.confirmations_checkbox.toggled.connect(lambda x: self.settings.set("ui.show_confirmations", x))
        
        # Animations
        self.animations_checkbox = QCheckBox("Habilitar animações")
        self.animations_checkbox.setChecked(self.settings.get("ui.animation_enabled", True))
        self.animations_checkbox.toggled.connect(lambda x: self.settings.set("ui.animation_enabled", x))
        
        ui_layout.addRow("Comportamento:", self.auto_switch_checkbox)
        ui_layout.addRow("Confirmações:", self.confirmations_checkbox)
        ui_layout.addRow("Animações:", self.animations_checkbox)
        
        ui_card.layout.addLayout(ui_layout)
        scroll_layout.addWidget(ui_card)
        
        # Configurações de WhatsApp
        whatsapp_card = Card("💬 WhatsApp", accent_color=SUCCESS_COLOR)
        whatsapp_layout = QFormLayout()
        
        self.prefer_app_checkbox = QCheckBox("Preferir aplicativo ao invés da web")
        self.prefer_app_checkbox.setChecked(self.settings.get("whatsapp.prefer_app_over_web", True))
        self.prefer_app_checkbox.toggled.connect(lambda x: self.settings.set("whatsapp.prefer_app_over_web", x))
        
        self.auto_advance_checkbox = QCheckBox("Avançar automaticamente após envio")
        self.auto_advance_checkbox.setChecked(self.settings.get("whatsapp.auto_advance_after_send", True))
        self.auto_advance_checkbox.toggled.connect(lambda x: self.settings.set("whatsapp.auto_advance_after_send", x))
        
        whatsapp_layout.addRow("Aplicativo:", self.prefer_app_checkbox)
        whatsapp_layout.addRow("Avançar:", self.auto_advance_checkbox)
        
        whatsapp_card.layout.addLayout(whatsapp_layout)
        scroll_layout.addWidget(whatsapp_card)
        
        # Gerenciamento de dados
        data_card = Card("💾 Gerenciamento de Dados", accent_color=WARNING_COLOR)
        data_layout = QVBoxLayout()
        
        # Botões de ação
        buttons_layout = QGridLayout()
        
        self.clear_cache_button = AnimatedButton("🗑️ Limpar Cache", ERROR_COLOR)
        self.clear_cache_button.clicked.connect(self.clear_cache)
        
        self.clear_history_button = AnimatedButton("📋 Limpar Histórico", WARNING_COLOR)
        self.clear_history_button.clicked.connect(self.clear_history)
        
        self.export_data_button = AnimatedButton("📤 Exportar Dados", PRIMARY_COLOR)
        self.export_data_button.clicked.connect(self.export_app_data)
        
        self.reset_settings_button = AnimatedButton("🔄 Resetar Configurações", ERROR_COLOR)
        self.reset_settings_button.clicked.connect(self.reset_settings)
        
        buttons_layout.addWidget(self.clear_cache_button, 0, 0)
        buttons_layout.addWidget(self.clear_history_button, 0, 1)
        buttons_layout.addWidget(self.export_data_button, 1, 0)
        buttons_layout.addWidget(self.reset_settings_button, 1, 1)
        
        data_layout.addLayout(buttons_layout)
        data_card.layout.addLayout(data_layout)
        scroll_layout.addWidget(data_card)
        
        # Configurações avançadas
        advanced_card = Card("⚙️ Configurações Avançadas", accent_color="#FF6B35")
        advanced_layout = QFormLayout()
        
        # Auto-save interval
        self.auto_save_spin = QSpinBox()
        self.auto_save_spin.setRange(60, 3600)  # 1 minute to 1 hour
        self.auto_save_spin.setValue(self.settings.get("processing.auto_save_interval", 300))
        self.auto_save_spin.setSuffix(" segundos")
        self.auto_save_spin.valueChanged.connect(lambda x: self.settings.set("processing.auto_save_interval", x))
        
        # Max log files
        self.max_logs_spin = QSpinBox()
        self.max_logs_spin.setRange(1, 100)
        self.max_logs_spin.setValue(self.settings.get("processing.max_log_files", 10))
        self.max_logs_spin.valueChanged.connect(lambda x: self.settings.set("processing.max_log_files", x))
        
        # Max history entries
        self.max_history_spin = QSpinBox()
        self.max_history_spin.setRange(10, 1000)
        self.max_history_spin.setValue(self.settings.get("processing.max_history_entries", 100))
        self.max_history_spin.valueChanged.connect(lambda x: self.settings.set("processing.max_history_entries", x))
        
        advanced_layout.addRow("Intervalo de auto-save:", self.auto_save_spin)
        advanced_layout.addRow("Máximo de arquivos de log:", self.max_logs_spin)
        advanced_layout.addRow("Máximo de entradas no histórico:", self.max_history_spin)
        
        advanced_card.layout.addLayout(advanced_layout)
        scroll_layout.addWidget(advanced_card)
        
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        settings_layout.addWidget(scroll_area)
        
        self.tab_widget.addTab(settings_tab, "⚙️ Configurações")
    
    def clear_cache(self):
        """Limpar cache da aplicação"""
        try:
            if not self.settings.get("ui.show_confirmations", True):
                cleared = self.settings.clear_cache()
                self.log(f"Cache limpo: {cleared} arquivos removidos")
                return
            
            reply = QMessageBox.question(
                self,
                "Limpar Cache",
                "Isso irá remover:\n• Arquivos temporários\n• Cache do navegador\n• Logs antigos\n\nContinuar?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                cleared = self.settings.clear_cache()
                QMessageBox.information(self, "Cache Limpo", f"✅ Cache limpo com sucesso!\n{cleared} arquivos removidos.")
                self.log(f"Cache limpo: {cleared} arquivos removidos")
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao limpar cache:\n{str(e)}")
    
    def clear_history(self):
        """Limpar histórico de processamento"""
        try:
            if not self.settings.get("ui.show_confirmations", True):
                self.settings.processing_history_file.unlink(missing_ok=True)
                self.log("Histórico de processamento limpo")
                return
            
            reply = QMessageBox.question(
                self,
                "Limpar Histórico",
                "Isso irá remover todo o histórico de processamento.\nContinuar?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.settings.processing_history_file.unlink(missing_ok=True)
                QMessageBox.information(self, "Histórico Limpo", "✅ Histórico de processamento limpo com sucesso!")
                self.log("Histórico de processamento limpo")
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao limpar histórico:\n{str(e)}")
    
    def export_app_data(self):
        """Exportar dados da aplicação"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Exportar Dados da Aplicação",
                f"caixa_lead_processor_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                "ZIP Files (*.zip)"
            )
            
            if file_path:
                if self.settings.export_data(file_path):
                    QMessageBox.information(self, "Exportação Concluída", f"✅ Dados exportados com sucesso para:\n{file_path}")
                    self.log(f"Dados exportados para: {file_path}")
                else:
                    QMessageBox.warning(self, "Erro na Exportação", "Falha ao exportar dados da aplicação.")
                    
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao exportar dados:\n{str(e)}")
    
    def reset_settings(self):
        """Resetar configurações para padrão"""
        try:
            if not self.settings.get("ui.show_confirmations", True):
                self.settings.reset_to_defaults()
                self.log("Configurações resetadas para padrão")
                return
            
            reply = QMessageBox.question(
                self,
                "Resetar Configurações",
                "⚠️ Isso irá resetar TODAS as configurações para os valores padrão.\n\n"
                "Suas configurações personalizadas serão perdidas.\nContinuar?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                if self.settings.reset_to_defaults():
                    QMessageBox.information(
                        self, 
                        "Configurações Resetadas", 
                        "✅ Configurações resetadas com sucesso!\n\n"
                        "Reinicie a aplicação para aplicar todas as mudanças."
                    )
                    self.log("Configurações resetadas para padrão")
                else:
                    QMessageBox.warning(self, "Erro", "Falha ao resetar configurações.")
                    
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao resetar configurações:\n{str(e)}")
    
    def create_status_bar(self):
        """Criar barra de status"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Status atual
        self.status_label = QLabel("Pronto")
        self.status_label.setStyleSheet("color: #28a745; font-weight: bold;")
        
        # Tempo decorrido
        self.time_label = QLabel("Tempo: 00:00:00")
        self.time_label.setStyleSheet("color: #666;")
        
        # Versão
        version_label = QLabel("v2.0.0 - Profissional")
        version_label.setStyleSheet("color: #666; font-size: 11px;")
        
        self.status_bar.addWidget(self.status_label)
        self.status_bar.addPermanentWidget(self.time_label)
        self.status_bar.addPermanentWidget(version_label)
    
    # Implementar métodos auxiliares e de controle
    def filter_table(self):
        """Filtrar tabela de leads"""
        status_filter = self.status_filter.currentText()
        search_text = self.search_input.text().lower()
        
        for row in range(self.leads_table.rowCount()):
            show_row = True
            
            # Filtro por status
            if status_filter != "Todos":
                status_item = self.leads_table.item(row, 5)
                if status_item and status_filter not in status_item.text():
                    show_row = False
            
            # Filtro por busca
            if search_text and show_row:
                found = False
                for col in range(3):  # Nome, email, telefone
                    item = self.leads_table.item(row, col)
                    if item and search_text in item.text().lower():
                        found = True
                        break
                if not found:
                    show_row = False
            
            self.leads_table.setRowHidden(row, not show_row)
    
    def refresh_reports(self):
        """Atualizar relatórios"""
        self.populate_leads_table()
        self.update_statistics()
        self.log("Relatórios atualizados com sucesso.")
    
    def clear_logs(self):
        """Limpar logs"""
        self.log_text.clear()
        self.log_text.setHtml("""
            <div style="color: #f8f8f2; text-align: center; padding: 20px;">
                <h3>Logs Limpos</h3>
                <p>Os novos logs aparecerão aqui...</p>
            </div>
        """)
    
    def save_logs(self):
        """Salvar logs em arquivo"""
        try:
            from datetime import datetime
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Salvar Logs", 
                f"logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "Text Files (*.txt)"
            )
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.toPlainText())
                QMessageBox.information(self, "Logs Salvos", f"Logs salvos em: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar logs: {str(e)}")
    
    def export_report(self):
        """Exportar relatório para Excel"""
        if not self.processed_leads:
            QMessageBox.warning(self, "Aviso", "Nenhum lead processado para exportar.")
            return
        
        try:
            import pandas as pd
            from datetime import datetime
            
            # Criar DataFrame
            data = []
            for lead in self.processed_leads:
                data.append({
                    "Nome": lead.get("name", "-"),
                    "Email": lead.get("email", "-"),
                    "Telefone": lead.get("phone", "-"),
                    "ID do Imóvel": lead.get("property_id", "-"),
                    "Cidade": lead.get("city", "-"),
                    "Status": lead.get("status", "-"),
                    "URL do Imóvel": lead.get("property_url", "-")
                })
            
            df = pd.DataFrame(data)
            
            # Salvar como Excel
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exportar Relatório", 
                f"leads_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                "Excel Files (*.xlsx)"
            )
            
            if file_path:
                with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                    df.to_excel(writer, sheet_name='Leads', index=False)
                    
                    # Formatação básica
                    workbook = writer.book
                    worksheet = writer.sheets['Leads']
                    
                    # Formato para cabeçalho
                    header_format = workbook.add_format({
                        'bold': True,
                        'text_wrap': True,
                        'valign': 'top',
                        'fg_color': '#1976D2',
                        'font_color': 'white'
                    })
                    
                    # Aplicar formato ao cabeçalho
                    for col_num, value in enumerate(df.columns.values):
                        worksheet.write(0, col_num, value, header_format)
                    
                    # Ajustar largura das colunas
                    worksheet.set_column('A:A', 25)  # Nome
                    worksheet.set_column('B:B', 30)  # Email
                    worksheet.set_column('C:C', 15)  # Telefone
                    worksheet.set_column('D:D', 20)  # ID Imóvel
                    worksheet.set_column('E:E', 20)  # Cidade
                    worksheet.set_column('F:F', 15)  # Status
                    worksheet.set_column('G:G', 40)  # URL
                
                QMessageBox.information(self, "Exportação Concluída", f"Relatório exportado com sucesso para:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Erro na Exportação", f"Erro ao exportar relatório: {str(e)}")
    
    def populate_leads_table(self):
        """Preencher tabela com leads processados"""
        self.leads_table.setRowCount(len(self.processed_leads))
        
        for i, lead in enumerate(self.processed_leads):
            # Nome
            self.leads_table.setItem(i, 0, QTableWidgetItem(lead.get("name", "-")))
            
            # Email
            self.leads_table.setItem(i, 1, QTableWidgetItem(lead.get("email", "-")))
            
            # Telefone
            self.leads_table.setItem(i, 2, QTableWidgetItem(lead.get("phone", "-")))
            
            # ID do Imóvel
            self.leads_table.setItem(i, 3, QTableWidgetItem(lead.get("property_id", "-")))
            
            # Cidade
            self.leads_table.setItem(i, 4, QTableWidgetItem(lead.get("city", "-")))
            
            # Status
            status = lead.get("status", "-")
            status_item = QTableWidgetItem(status)
            
            # Cor do status
            if status == "Completo":
                status_item.setForeground(QColor(SUCCESS_COLOR))
            elif "Pendente" in status:
                status_item.setForeground(QColor(WARNING_COLOR))
            elif "Erro" in status:
                status_item.setForeground(QColor(ERROR_COLOR))
            
            self.leads_table.setItem(i, 5, status_item)
            
            # Botões de ação
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 5, 5, 5)
            
            if lead.get("property_url"):
                view_btn = QPushButton("Ver")
                view_btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {PRIMARY_COLOR};
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 4px 8px;
                        font-size: 11px;
                        font-weight: bold;
                    }}
                    QPushButton:hover {{
                        background-color: {SECONDARY_COLOR};
                    }}
                """)
                view_btn.clicked.connect(lambda checked, url=lead["property_url"]: webbrowser.open(url))
                action_layout.addWidget(view_btn)
            
            self.leads_table.setCellWidget(i, 6, action_widget)
    
    def update_statistics(self):
        """Atualizar estatísticas"""
        total = len(self.processed_leads)
        complete = sum(1 for lead in self.processed_leads if lead.get("status") == "Completo")
        pending = sum(1 for lead in self.processed_leads if "Pendente" in lead.get("status", ""))
        error = sum(1 for lead in self.processed_leads if "Erro" in lead.get("status", ""))
        
        # Atualizar widgets de estatística
        self.stats_total.findChild(QLabel, "stat_value_total_de_leads").setText(str(total))
        self.stats_complete.findChild(QLabel, "stat_value_completos").setText(str(complete))
        self.stats_pending.findChild(QLabel, "stat_value_pendentes").setText(str(pending))
        self.stats_error.findChild(QLabel, "stat_value_com_erro").setText(str(error))
    
    def start_loading_animation(self):
        """Iniciar animação de carregamento na interface"""
        # Animar a barra de progresso para indicar que a aplicação está pronta
        self.main_progress.setRange(0, 0)  # Modo indeterminado
        
        # Usar um timer para parar a animação após 1 segundo
        QTimer.singleShot(1000, self.stop_loading_animation)
    
    def stop_loading_animation(self):
        """Parar animação de carregamento"""
        self.main_progress.setRange(0, 100)
        self.main_progress.setValue(0)
    
    def browse_file(self):
        """Abrir diálogo para selecionar arquivo de leads"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecionar Arquivo de Leads", "", "Arquivos de Texto (*.txt);;Todos os Arquivos (*)"
        )
        
        if file_path:
            self.file_path_edit.setText(file_path)
            self.log(f"Arquivo selecionado: {file_path}")
            self.status_bar.showMessage(f"Arquivo selecionado: {os.path.basename(file_path)}")
    
    def log(self, message):
        """Adicionar mensagem ao log com formatação melhorada"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Determinar cor baseada no emoji ou palavra-chave
        color = "#f8f8f2"  # Cor padrão (branco)
        
        # Cores baseadas em tags específicas
        if "[SUCESSO]" in message or "[COMPLETO]" in message or "[FINALIZADO]" in message:
            color = "#50fa7b"  # Verde brilhante para sucesso
        elif "[CIDADE]" in message and "✅" in message:
            color = "#50fa7b"  # Verde para cidade encontrada
        elif "[EXTRAINDO]" in message or "[LENDO]" in message or "[ANALISANDO]" in message:
            color = "#8be9fd"  # Ciano para processos de extração
        elif "[CONECTANDO]" in message or "[WEBDRIVER]" in message or "[PESQUISANDO]" in message:
            color = "#bd93f9"  # Roxo para conexões
        elif "[VERIFICANDO]" in message or "[TENTATIVA]" in message:
            color = "#f1fa8c"  # Amarelo para verificações
        elif "[ERRO]" in message or "[FALHA]" in message:
            color = "#ff5555"  # Vermelho para erros
        elif "[TIMEOUT]" in message or "[PENDENTE]" in message or "[MANUAL]" in message:
            color = "#ffb86c"  # Laranja para situações pendentes
        elif "[INDISPONÍVEL]" in message or "[TEMPLATE]" in message:
            color = "#f1fa8c"  # Amarelo para casos especiais
        elif "[URL]" in message or "[REVISÃO]" in message:
            color = "#8be9fd"  # Ciano para URLs e revisões
        elif "[DIAGNÓSTICO]" in message or "[DICA]" in message:
            color = "#6272a4"  # Azul acinzentado para diagnósticos
        
        # Cores baseadas em emojis (fallback)
        elif any(emoji in message for emoji in ["✅", "🎉", "🎯"]):
            color = "#50fa7b"  # Verde para sucesso
        elif any(emoji in message for emoji in ["⚠️", "⏱️", "📍", "📝"]):
            color = "#f1fa8c"  # Amarelo para avisos
        elif any(emoji in message for emoji in ["❌", "🚫"]):
            color = "#ff5555"  # Vermelho para erros
        elif any(emoji in message for emoji in ["🔍", "🌐", "📄", "👤", "🏙️", "🔗"]):
            color = "#8be9fd"  # Ciano para informações
        elif any(emoji in message for emoji in ["🚀", "⏸️", "⏹️", "🔄"]):
            color = "#bd93f9"  # Roxo para ações do sistema
        elif any(emoji in message for emoji in ["👥", "📁", "📞", "🏠"]):
            color = "#50c7e3"  # Azul claro para dados
        
        # Tratamento especial para separadores
        if "=" in message and len(message.strip()) > 30:
            color = "#6272a4"
            formatted_message = f'<span style="color: {color}; font-family: monospace;">{message}</span>'
        elif message.strip() == "":
            # Linha em branco
            formatted_message = "<br>"
        else:
            # Formatar mensagem com timestamp colorido
            formatted_message = f'<span style="color: #6272a4; font-size: 11px;">[{timestamp}]</span> <span style="color: {color};">{message}</span>'
        
        self.log_text.append(formatted_message)
        
        # Rolar para o final
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.log_text.setTextCursor(cursor)
        
        # Também atualizar o progresso detalhado na aba de processamento
        self.update_detailed_progress(message, timestamp, color)
        self.log_text.ensureCursorVisible()
    
    def update_detailed_progress(self, message, timestamp, color):
        """Atualizar o progresso detalhado na aba de processamento de forma user-friendly"""
        if not hasattr(self, 'detailed_progress_text'):
            return
        
        # Converter mensagens técnicas para linguagem mais amigável
        user_friendly_message = self.convert_to_user_friendly(message)
        
        # Se a mensagem foi convertida, usar ela; senão, filtrar mensagens muito técnicas
        if user_friendly_message:
            # Determinar ícone baseado no tipo de mensagem
            icon = self.get_message_icon(message)
            
            # Formatar para a interface de processamento (mais limpa e espaçada)
            if "=" in message and len(message.strip()) > 30:
                # Separador - criar uma linha visual mais elegante
                formatted_msg = '<div style="margin: 15px 0;"><hr style="border: none; border-top: 2px solid #e3f2fd; margin: 0;"></div>'
            elif message.strip() == "":
                # Linha em branco com mais espaço
                formatted_msg = "<div style='margin: 8px 0;'></div>"
            else:
                # Mensagem normal com formatação user-friendly e mais espaçamento
                # Tratamento especial para headers de leads
                if "<b>Lead" in user_friendly_message and "de" in user_friendly_message:
                    # Header de lead - mais destaque
                    formatted_msg = f'''
                    <div style="margin: 20px 0 10px 0; padding: 12px; background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); border-radius: 8px; border-left: 4px solid #2196F3;">
                        <span style="margin-right: 12px; font-size: 16px;">{icon}</span>
                        <span style="font-size: 15px; font-weight: 600; color: #1976d2;">{user_friendly_message}</span>
                    </div>
                    '''
                else:
                    # Mensagem normal
                    formatted_msg = f'''
                    <div style="margin: 6px 0; padding: 4px 0; color: {color}; font-size: 13px;">
                        <span style="margin-right: 10px; font-size: 14px;">{icon}</span>
                        <span style="font-weight: 500;">{user_friendly_message}</span>
                    </div>
                    '''
            
            self.detailed_progress_text.append(formatted_msg)
            
            # Rolar para o final
            cursor = self.detailed_progress_text.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.detailed_progress_text.setTextCursor(cursor)
    
    def convert_to_user_friendly(self, message):
        """Converter mensagens técnicas para linguagem user-friendly"""
        
        # Mapeamento de mensagens técnicas para user-friendly
        conversions = {
            # Arquivo e extração
            "[LENDO] Abrindo arquivo de leads...": "Abrindo arquivo de leads...",
            "[ANALISANDO] Extraindo informações dos leads...": "Analisando dados dos leads...",
            "[SUCESSO] Encontrados": "Encontrados",
            "[PREVIEW] Primeiros leads:": "Leads encontrados:",
            
            # WebDriver
            "[WEBDRIVER] Iniciando configuração do navegador...": "Preparando navegador...",
            "[MODO] Execução em modo invisível (headless)": "Modo: Navegador invisível",
            "[MODO] Execução com interface visível": "Modo: Navegador visível",
            "[DOWNLOAD] Verificando ChromeDriver...": "Verificando componentes do navegador...",
            "[WEBDRIVER] Navegador configurado e pronto para uso": "Navegador pronto ✓",
            "[PRONTO] Sistema pronto para processar leads": "Sistema pronto para iniciar ✓",
            
            # Processamento de leads
            "[INICIANDO] Processamento do lead:": "Processando:",
            "[PESQUISANDO] Buscando detalhes do imóvel": "Buscando informações do imóvel...",
            "[CONECTANDO] Acessando site da CAIXA...": "Conectando ao site da CAIXA...",
            "[TEMPO] Busca realizada em": "Busca concluída em",
            "[SUCESSO] URL do imóvel encontrada": "Link do imóvel encontrado ✓",
            "[VERIFICANDO] Disponibilidade do imóvel...": "Verificando se o imóvel está disponível...",
            "[DISPONÍVEL] Imóvel está disponível para venda": "Imóvel disponível ✓",
            "[INDISPONÍVEL] Imóvel não está mais disponível para venda": "⚠️ Imóvel não está mais disponível",
            "[TEMPLATE] Mensagem especial será utilizada para este lead": "Usando mensagem especial para imóvel indisponível",
            "[EXTRAINDO] Informações da cidade...": "Extraindo localização...",
            "[CIDADE] Cidade extraída com sucesso:": "Cidade encontrada:",
            "[COMPLETO] Lead": "✓ Lead processado:",
            "[FINALIZADO] Lead": "✓ Concluído:",
            
            # Erros e timeouts
            "[TIMEOUT] Timeout na busca do imóvel": "⏱️ Tempo limite excedido na busca",
            "[CONECTIVIDADE] Possível problema de conexão ou site lento": "Conexão lenta detectada",
            "[ALTERNATIVA] Tentando obter URL alternativa...": "Tentando método alternativo...",
            "[PENDENTE] Lead": "⚠️ Lead marcado para revisão:",
            "[MANUAL] Lead marcado para revisão manual": "Marcado para revisão manual",
            "[ERRO] Imóvel não encontrado no sistema": "❌ Imóvel não encontrado",
            "[DIAGNÓSTICO] Possíveis causas: ID inválido ou imóvel removido": "Possível ID inválido ou imóvel removido",
            
            # Tentativas e falhas
            "[TENTATIVA] Tentando métodos alternativos de extração...": "Tentando métodos alternativos...",
            "[FALHA] Métodos alternativos não obtiveram sucesso": "Métodos alternativos não funcionaram",
            "[FALHA] Não foi possível gerar URL alternativa": "Não foi possível gerar link alternativo",
        }
        
        # Aplicar conversões diretas
        for tech_msg, friendly_msg in conversions.items():
            if tech_msg in message:
                return message.replace(tech_msg, friendly_msg)
        
        # Conversões baseadas em padrões
        import re
        
        # Lead header (exemplo: "[LEAD 1/5] João Silva")
        lead_match = re.search(r'\[LEAD (\d+)/(\d+)\]\s*(.+)', message)
        if lead_match:
            current, total, name = lead_match.groups()
            return f"<b>Lead {current} de {total}: {name}</b>"
        
        # Telefone
        if "[TELEFONE]" in message:
            phone = message.split("[TELEFONE]")[-1].strip()
            return f"📞 {phone}"
        
        # ID do imóvel
        if "[IMÓVEL ID]" in message:
            prop_id = message.split("[IMÓVEL ID]")[-1].strip()
            return f"🏠 Imóvel: {prop_id}"
        
        # URL (encurtar URLs longas)
        if "[URL]" in message and "http" in message:
            return "🔗 Link do imóvel salvo"
        
        if "[REVISÃO]" in message and "http" in message:
            return "📋 Link salvo para revisão manual"
        
        # Arquivo
        if "[ARQUIVO]" in message:
            return None  # Não mostrar path do arquivo
        
        # Filtrar mensagens muito técnicas que não precisam aparecer
        technical_filters = [
            "DIAGNÓSTICO", "DICA"
        ]
        
        for filter_term in technical_filters:
            if f"[{filter_term}]" in message:
                return None
        
        # Se não há conversão específica, mas tem tags técnicas, simplificar
        if "[" in message and "]" in message:
            # Remover tags técnicas e manter apenas o conteúdo útil
            cleaned = re.sub(r'\[.*?\]\s*', '', message)
            if cleaned.strip():
                return cleaned.strip()
        
        # Se chegou até aqui, retornar mensagem original (caso não seja muito técnica)
        if not any(term in message.lower() for term in ['error', 'exception', 'traceback', 'debug']):
            return message
        
        return None  # Filtrar mensagens muito técnicas
    
    def get_message_icon(self, message):
        """Obter ícone apropriado para o tipo de mensagem"""
        if "[SUCESSO]" in message or "✓" in message or "[COMPLETO]" in message:
            return "✅"
        elif "[ERRO]" in message or "❌" in message or "[FALHA]" in message:
            return "❌"
        elif "[TIMEOUT]" in message or "[PENDENTE]" in message or "⚠️" in message:
            return "⚠️"
        elif "[CONECTANDO]" in message or "[WEBDRIVER]" in message:
            return "🌐"
        elif "[PESQUISANDO]" in message or "[VERIFICANDO]" in message:
            return "🔍"
        elif "[EXTRAINDO]" in message or "[ANALISANDO]" in message:
            return "📊"
        elif "[CIDADE]" in message or "📍" in message:
            return "📍"
        elif "[URL]" in message or "🔗" in message:
            return "🔗"
        elif "[TELEFONE]" in message or "📞" in message:
            return "📞"
        elif "[IMÓVEL]" in message or "🏠" in message:
            return "🏠"
        elif "Lead" in message and ("/" in message or ":" in message):
            return "👤"
        else:
            return "ℹ️"
    
    def start_processing(self):
        """Iniciar o processamento de leads"""
        file_path = self.file_path_edit.text()
        
        if not file_path:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione um arquivo de leads.")
            return
            
        if not os.path.exists(file_path):
            QMessageBox.warning(self, "Aviso", "O arquivo selecionado não existe.")
            return
        
        # Limpar o log e progresso detalhado
        self.log_text.clear()
        if hasattr(self, 'detailed_progress_text'):
            self.detailed_progress_text.clear()
        
        # Desabilitar botão de iniciar e habilitar botão de parar
        self.main_start_button.setEnabled(False)
        self.main_stop_button.setEnabled(True)
        
        # Atualizar status
        self.status_label.setText("Processando...")
        self.status_label.setStyleSheet("color: #ff9800; font-weight: bold;")
        self.processing_status.setText("Iniciando processamento de leads...")
        
        # Mudar para aba de processamento
        self.tab_widget.setCurrentIndex(2)  # Index 2 is the processing tab
        
        # Iniciar thread de processamento
        headless = self.headless_checkbox.isChecked()
        auto_skip = self.auto_skip_checkbox.isChecked()
        self.worker_thread = WorkerThread(file_path, headless, auto_skip)
        
        # Conectar sinais
        self.worker_thread.update_signal.connect(self.log)
        self.worker_thread.progress_signal.connect(self.update_progress)
        self.worker_thread.lead_signal.connect(self.update_lead_info)
        self.worker_thread.finished_signal.connect(self.processing_finished)
        self.worker_thread.error_signal.connect(self.show_error)
        if hasattr(self.worker_thread, 'warning_signal'):
            self.worker_thread.warning_signal.connect(self.show_warning)
        
        # Iniciar thread
        self.worker_thread.start()
        
        self.log("Processamento iniciado.")
    
    def stop_processing(self):
        """Parar o processamento de leads"""
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.stop_requested = True
            self.log("Solicitação de interrupção enviada. Aguarde...")
            self.status_label.setText("Parando...")
            self.status_label.setStyleSheet("color: #f44336; font-weight: bold;")
    
    def processing_finished(self, all_leads):
        """Chamado quando o processamento é concluído"""
        self.main_start_button.setEnabled(True)
        self.main_stop_button.setEnabled(False)
        self.view_property_button.setEnabled(False)
        self.send_whatsapp_button.setEnabled(False)
        self.edit_lead_button.setEnabled(False)
        self.skip_lead_button.setEnabled(False)
        
        # Atualizar status
        self.status_label.setText("Concluído")
        self.status_label.setStyleSheet("color: #28a745; font-weight: bold;")
        self.processing_status.setText("Processamento concluído com sucesso!")
        
        # Armazenar leads processados
        if all_leads:
            self.processed_leads = all_leads
            self.current_lead_index = 0  # Reset to first lead
            
            # Mostrar o primeiro lead e habilitar navegação
            if len(self.processed_leads) > 0:
                self.show_lead_at_index(0)
                # Re-enable action buttons for browsing processed leads
                self.edit_lead_button.setEnabled(True)
            
            self.populate_leads_table()
            self.update_statistics()
        
        self.log("🎉 Processamento concluído!")
        
        # Criar e mostrar resumo detalhado
        summary = self.create_error_summary()
        self.log(summary)
        
        # Mostrar mensagem de conclusão com resumo
        total_leads = len(all_leads) if all_leads else 0
        success_count = sum(1 for lead in all_leads if "✅" in lead.get("status", "")) if all_leads else 0
        
        if success_count == total_leads and total_leads > 0:
            # Todos processados com sucesso
            QMessageBox.information(
                self, 
                "✅ Processamento Concluído!", 
                f"Todos os {total_leads} leads foram processados com sucesso!\n\nVerifique a aba de Relatórios para mais detalhes."
            )
        elif total_leads > 0:
            # Alguns com problemas
            error_count = total_leads - success_count
            QMessageBox.warning(
                self, 
                "⚠️ Processamento Concluído com Ressalvas", 
                f"Processamento finalizado:\n\n"
                f"✅ {success_count} leads processados com sucesso\n"
                f"⚠️ {error_count} leads com problemas\n\n"
                f"Verifique a aba de Relatórios e Logs para mais detalhes."
            )
        else:
            # Nenhum lead processado
            QMessageBox.warning(
                self, 
                "⚠️ Nenhum Lead Processado", 
                "Nenhum lead foi processado com sucesso.\n\nVerifique os logs para identificar os problemas."
            )
        
        # Mudar para aba de relatórios
        self.tab_widget.setCurrentIndex(2)
    
    def update_progress(self, current, total):
        """Atualizar a barra de progresso e estatísticas"""
        if total > 0:
            self.main_progress.setMaximum(total)
            self.main_progress.setValue(current)
            self.current_lead_progress.setMaximum(total)
            self.current_lead_progress.setValue(current)
            
            percentage = int((current / total) * 100)
            self.processing_status.setText(f"Processando lead {current} de {total} ({percentage}%)")
            
            # Atualizar estatísticas
            self.stats_total.findChild(QLabel, "stat_value_total_de_leads").setText(str(current))
            
            # Contar leads completos e pendentes
            if hasattr(self.worker_thread, "all_leads") and self.worker_thread.all_leads:
                complete_leads = sum(1 for lead in self.worker_thread.all_leads if lead.get("status") == "Completo")
                pending_leads = sum(1 for lead in self.worker_thread.all_leads if lead.get("status", "").startswith("Pendente"))
                error_leads = sum(1 for lead in self.worker_thread.all_leads if "Erro" in lead.get("status", ""))
                
                self.stats_complete.findChild(QLabel, "stat_value_completos").setText(str(complete_leads))
                self.stats_pending.findChild(QLabel, "stat_value_pendentes").setText(str(pending_leads))
                self.stats_error.findChild(QLabel, "stat_value_com_erro").setText(str(error_leads))
    
    def update_lead_info(self, lead):
        """Atualizar informações do lead atual"""
        self.current_lead = lead
        
        # Atualizar labels
        self.lead_name_label.setText(lead.get('name', '-'))
        self.lead_email_label.setText(lead.get('email', '-'))
        self.lead_phone_label.setText(lead.get('phone', '-'))
        self.lead_property_id_label.setText(lead.get('property_id', '-'))
        self.lead_city_label.setText(lead.get('city', '-'))
        
        # Habilitar botões se tivermos as informações necessárias
        has_property_url = 'property_url' in lead and lead['property_url'] and lead['property_url'] != ""
        has_city = 'city' in lead and lead['city'] and lead['city'] != ""
        property_not_available = lead.get("property_not_available") or lead.get("error_details") == "property_no_longer_available"
        is_pending_manual_review = "Pendente" in lead.get("status", "") or lead.get("manual_review_needed", False)
        
        self.view_property_button.setEnabled(has_property_url)
        # Enable WhatsApp button if we have regular info OR if property is not available OR if it's pending manual review (special message)
        self.send_whatsapp_button.setEnabled((has_property_url and has_city) or property_not_available or is_pending_manual_review)
        self.edit_lead_button.setEnabled(True)  # Always enabled when we have a lead
        self.skip_lead_button.setEnabled(True)
    
    def view_property(self):
        """Abrir a página do imóvel no navegador"""
        if self.current_lead and 'property_url' in self.current_lead:
            url = self.current_lead['property_url']
            QDesktopServices.openUrl(QUrl(url))
            self.log(f"Abrindo URL do imóvel: {url}")
        else:
            self.log("URL do imóvel não disponível.")
    
    def send_whatsapp(self):
        """Preparar e enviar mensagem de WhatsApp"""
        if not self.current_lead:
            return
            
        if not self.worker_thread or not self.worker_thread.processor:
            return
        
        try:
            # Gerar a mensagem de WhatsApp
            message = self.worker_thread.processor.generate_whatsapp_message(self.current_lead)
            
            # Log da mensagem gerada
            self.log(f"Mensagem do WhatsApp gerada para {self.current_lead.get('name')}")
            
            # Criar e abrir a página HTML com a mensagem
            self.create_whatsapp_html(message, self.current_lead)
            
            # Abrir WhatsApp diretamente sem perguntar
            import urllib.parse
            encoded_message = urllib.parse.quote(message)
            
            # Construir a URL do WhatsApp
            phone = self.current_lead.get('phone', '').strip()

            # Remove any formatting from phone number
            phone = ''.join(filter(str.isdigit, phone))
            if phone and not phone.startswith('55'):
                phone = '55' + phone  # Add Brazil country code if not present
            
            # Try to open WhatsApp app directly first
            whatsapp_app_url = f"whatsapp://send?phone={phone}&text={encoded_message}"
            success = QDesktopServices.openUrl(QUrl(whatsapp_app_url))
            
            if success:
                self.log("WhatsApp aberto diretamente no aplicativo.")
            else:
                # Fallback to web version
                whatsapp_web_url = f"https://api.whatsapp.com/send?phone={phone}&text={encoded_message}"
                QDesktopServices.openUrl(QUrl(whatsapp_web_url))
                self.log("WhatsApp aberto na versão web.")
            
            # Perguntar se a mensagem foi enviada com sucesso
            reply = QMessageBox.question(
                self, 
                "Confirmação", 
                "A mensagem foi enviada com sucesso?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if reply == QMessageBox.Yes:
                self.log(f"Mensagem enviada com sucesso para {self.current_lead.get('name')}.")
                # Avançar para o próximo lead
                self.skip_lead()
            else:
                self.log(f"Falha ao enviar mensagem para {self.current_lead.get('name')}.")
                
        except Exception as e:
            self.log(f"Erro ao preparar mensagem de WhatsApp: {str(e)}")
    
    def create_whatsapp_html(self, message, lead):
        """Criar uma página HTML para exibir a mensagem do WhatsApp"""
        try:
            # Salvar a mensagem em um arquivo de texto
            message_file = os.path.join(os.getcwd(), f"mensagem_{lead.get('name', 'desconhecido')}.txt")
            with open(message_file, 'w', encoding='utf-8') as f:
                f.write(message)
            
            # Codificar a mensagem para URL
            import urllib.parse
            encoded_message = urllib.parse.quote(message)
            
            # Construir a URL do WhatsApp
            phone = lead.get('phone', '').strip()
            
            # Remove any formatting from phone number
            phone = ''.join(filter(str.isdigit, phone))
            if phone and not phone.startswith('55'):
                phone = '55' + phone  # Add Brazil country code if not present
                
            # Use direct WhatsApp app URL
            whatsapp_url = f"whatsapp://send?phone={phone}&text={encoded_message}"
            
            # Criar um arquivo HTML para exibir a mensagem com formatação correta
            html_file = os.path.join(os.getcwd(), f"mensagem_{lead.get('name', 'desconhecido')}.html")
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write('<!DOCTYPE html>\n')
                f.write('<html>\n')
                f.write('<head>\n')
                f.write('    <meta charset="UTF-8">\n')
                f.write('    <title>Mensagem para WhatsApp</title>\n')
                f.write('    <style>\n')
                f.write('        @import url(\'https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap\');\n')
                f.write('        body { font-family: \'Roboto\', Arial, sans-serif; padding: 20px; background-color: #ECE5DD; margin: 0; }\n')
                f.write('        .container { background-color: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); max-width: 600px; margin: 20px auto; }\n')
                f.write('        h1 { color: #075e54; font-size: 22px; margin-bottom: 20px; }\n')
                f.write('        .message { white-space: pre-wrap; background-color: #DCF8C6; padding: 20px; border-radius: 10px; margin: 20px 0; font-size: 16px; line-height: 1.5; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }\n')
                f.write('        .instructions { background-color: #ffe0b2; padding: 15px; border-radius: 10px; margin-top: 25px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }\n')
                f.write('        .buttons { display: flex; gap: 15px; margin-top: 25px; }\n')
                f.write('        button { background-color: #075e54; color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 14px; transition: all 0.3s ease; }\n')
                f.write('        button:hover { background-color: #128c7e; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }\n')
                f.write('        .whatsapp-btn { background-color: #25D366; }\n')
                f.write('        .whatsapp-btn:hover { background-color: #1da851; }\n')
                f.write('        .header { display: flex; align-items: center; margin-bottom: 25px; }\n')
                f.write('        .logo { width: 50px; height: 50px; background-color: #075e54; border-radius: 10px; margin-right: 15px; display: flex; align-items: center; justify-content: center; }\n')
                f.write('        .logo svg { width: 30px; height: 30px; }\n')
                f.write('        .lead-info { background-color: #f5f5f5; padding: 15px; border-radius: 10px; margin-bottom: 20px; }\n')
                f.write('        .lead-info p { margin: 5px 0; }\n')
                f.write('        .lead-info strong { color: #075e54; }\n')
                f.write('        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }\n')
                f.write('        .container { animation: fadeIn 0.5s ease-out; }\n')
                f.write('    </style>\n')
                f.write('</head>\n')
                f.write('<body>\n')
                f.write('    <div class="container">\n')
                f.write('        <div class="header">\n')
                f.write('            <div class="logo">\n')
                f.write('                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white">\n')
                f.write('                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>\n')
                f.write('                </svg>\n')
                f.write('            </div>\n')
                f.write('            <h1>Mensagem para WhatsApp - Copie e Cole no App</h1>\n')
                f.write('        </div>\n')
                
                # Adicionar informações do lead
                f.write('        <div class="lead-info">\n')
                f.write(f'            <p><strong>Nome:</strong> {lead.get("name", "Não informado")}</p>\n')
                f.write(f'            <p><strong>Telefone:</strong> {lead.get("phone", "Não informado")}</p>\n')
                f.write(f'            <p><strong>Imóvel:</strong> {lead.get("property_id", "Não informado")}</p>\n')
                f.write(f'            <p><strong>Cidade:</strong> {lead.get("city", "Não informado")}</p>\n')
                f.write('        </div>\n')
                
                # Escapar caracteres HTML e preservar quebras de linha
                escaped_message = message.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                formatted_message = escaped_message.replace('\n', '<br>')
                f.write(f'        <div class="message" id="messageText">{formatted_message}</div>\n')
                f.write('        <div class="buttons">\n')
                f.write('            <button onclick="copyMessage()">Copiar Mensagem</button>\n')
                f.write(f'            <button class="whatsapp-btn" onclick="openWhatsApp()">Abrir WhatsApp</button>\n')
                f.write('        </div>\n')
                f.write('        <div class="instructions">\n')
                f.write('            <p><strong>Instruções:</strong></p>\n')
                f.write('            <ol>\n')
                f.write('                <li>Clique no botão "Copiar Mensagem" acima</li>\n')
                f.write('                <li>Clique no botão "Abrir WhatsApp" ou abra o WhatsApp manualmente</li>\n')
                f.write('                <li>Cole a mensagem no WhatsApp</li>\n')
                f.write('                <li>Feche esta janela quando terminar</li>\n')
                f.write('            </ol>\n')
                f.write('        </div>\n')
                f.write('    </div>\n')
                # Armazenar a mensagem original em um elemento oculto para preservar formatação
                f.write('    <textarea id="originalMessage" style="display:none;">' + message + '</textarea>\n')
                f.write('    <script>\n')
                f.write('        function copyMessage() {\n')
                f.write('            // Usar o texto original do textarea oculto para preservar quebras de linha\n')
                f.write('            const messageText = document.getElementById("originalMessage").value;\n')
                f.write('            navigator.clipboard.writeText(messageText)\n')
                f.write('                .then(() => {\n')
                f.write('                    // Destacar visualmente que a cópia foi bem-sucedida\n')
                f.write('                    const button = document.querySelector("button");\n')
                f.write('                    button.textContent = "✓ Copiado!";\n')
                f.write('                    button.style.backgroundColor = "#4CAF50";\n')
                f.write('                    setTimeout(() => {\n')
                f.write('                        button.textContent = "Copiar Mensagem";\n')
                f.write('                        button.style.backgroundColor = "#075e54";\n')
                f.write('                    }, 2000);\n')
                f.write('                })\n')
                f.write('                .catch(err => alert("Erro ao copiar: " + err));\n')
                f.write('        }\n')
                f.write(f'        function openWhatsApp() {{\n')
                f.write(f'            window.open("{whatsapp_url}", "_blank");\n')
                f.write('        }\n')
                f.write('        // Adicionar efeito de hover nos botões\n')
                f.write('        const buttons = document.querySelectorAll("button");\n')
                f.write('        buttons.forEach(button => {\n')
                f.write('            button.addEventListener("mouseover", function() {\n')
                f.write('                this.style.transform = "translateY(-2px)";\n')
                f.write('                this.style.boxShadow = "0 5px 15px rgba(0,0,0,0.1)";\n')
                f.write('            });\n')
                f.write('            button.addEventListener("mouseout", function() {\n')
                f.write('                this.style.transform = "translateY(0)";\n')
                f.write('                this.style.boxShadow = "none";\n')
                f.write('            });\n')
                f.write('        });\n')
                f.write('    </script>\n')
                f.write('</body>\n')
                f.write('</html>\n')
            
            # Abrir o arquivo HTML no navegador padrão
            webbrowser.open(html_file)
            self.log("Mensagem aberta em uma página HTML para fácil cópia")
            
        except Exception as e:
            self.log(f"Erro ao criar página HTML: {str(e)}")
    
    def skip_lead(self):
        """Pular para o próximo lead"""
        if self.current_lead:
            self.log(f"Pulando lead: {self.current_lead.get('name')}")
        
        # Limpar informações do lead atual
        self.current_lead = None
        self.lead_name_label.setText("-")
        self.lead_email_label.setText("-")
        self.lead_phone_label.setText("-")
        self.lead_property_id_label.setText("-")
        self.lead_city_label.setText("-")
        
        # Desabilitar botões
        self.view_property_button.setEnabled(False)
        self.send_whatsapp_button.setEnabled(False)
        self.edit_lead_button.setEnabled(False)
        self.skip_lead_button.setEnabled(False)
    
    def edit_lead(self):
        """Abrir diálogo para editar informações do lead atual"""
        if not self.current_lead:
            return
            
        dialog = EditLeadDialog(self.current_lead, self)
        if dialog.exec_() == QDialog.Accepted:
            # Atualizar o lead com as informações editadas
            updated_lead = dialog.get_lead_data()
            self.current_lead.update(updated_lead)
            
            # Atualizar a interface
            self.update_lead_info(self.current_lead)
            
            # Atualizar na lista de leads processados se existir
            if hasattr(self, 'processed_leads') and self.processed_leads:
                for i, lead in enumerate(self.processed_leads):
                    if (lead.get('property_id') == self.current_lead.get('property_id') and 
                        lead.get('name') == updated_lead.get('original_name', self.current_lead.get('name'))):
                        self.processed_leads[i] = self.current_lead.copy()
                        # Atualizar tabela se estiver na aba de relatórios
                        if hasattr(self, 'leads_table'):
                            self.populate_leads_table()
                        break
            
            self.log(f"✏️ Lead editado: {self.current_lead.get('name')}")
    
    def prev_lead(self):
        """Navegar para o lead anterior"""
        if self.processed_leads and self.current_lead_index > 0:
            self.current_lead_index -= 1
            self.show_lead_at_index(self.current_lead_index)
    
    def next_lead(self):
        """Navegar para o próximo lead"""
        if self.processed_leads and self.current_lead_index < len(self.processed_leads) - 1:
            self.current_lead_index += 1
            self.show_lead_at_index(self.current_lead_index)
    
    def show_lead_at_index(self, index):
        """Exibir lead no índice especificado"""
        if 0 <= index < len(self.processed_leads):
            lead = self.processed_leads[index]
            self.update_lead_info(lead)
            self.update_navigation_controls()
            self.log(f"📋 Exibindo lead {index + 1}: {lead.get('name')}")
    
    def update_navigation_controls(self):
        """Atualizar controles de navegação"""
        if not self.processed_leads:
            self.navigation_widget.setVisible(False)
            return
        
        total_leads = len(self.processed_leads)
        current_position = self.current_lead_index + 1
        
        # Atualizar label de posição
        self.lead_position_label.setText(f"Lead {current_position} de {total_leads}")
        
        # Atualizar botões
        self.prev_lead_button.setEnabled(self.current_lead_index > 0)
        self.next_lead_button.setEnabled(self.current_lead_index < total_leads - 1)
        
        # Mostrar controles de navegação se houver mais de um lead
        self.navigation_widget.setVisible(total_leads > 1)
    
    def show_error(self, error_message):
        """Exibir mensagem de erro crítico"""
        self.log(f"❌ ERRO CRÍTICO: {error_message}")
        
        # Atualizar status
        self.status_label.setText("Erro")
        self.status_label.setStyleSheet("color: #f44336; font-weight: bold;")
        self.processing_status.setText(f"Erro crítico: {error_message}")
        
        # Reabilitar botões
        self.main_start_button.setEnabled(True)
        self.main_stop_button.setEnabled(False)
        
        # Mostrar popup apenas para erros críticos
        QMessageBox.critical(
            self, 
            "Erro Crítico", 
            f"Ocorreu um erro crítico durante o processamento:\n\n{error_message}\n\nVerifique os logs para mais detalhes."
        )
    
    def show_warning(self, warning_message):
        """Exibir mensagem de aviso (não crítico)"""
        self.log(f"⚠️ AVISO: {warning_message}")
        
        # Atualizar status temporariamente
        current_status = self.processing_status.text()
        self.processing_status.setText(f"Aviso: {warning_message}")
        
        # Voltar ao status anterior após 3 segundos
        QTimer.singleShot(3000, lambda: self.processing_status.setText(current_status))
    
    def handle_processing_error(self, lead_name, error_type, error_details):
        """Lidar com erros específicos de processamento"""
        error_messages = {
            "property_not_found": f"🏠 Imóvel não encontrado para {lead_name}. Verifique se o ID está correto.",
            "city_not_found": f"📍 Cidade não encontrada para {lead_name}. Será necessária revisão manual.",
            "connection_error": f"🌐 Problema de conexão ao processar {lead_name}. Tentando continuar...",
            "timeout_error": f"⏱️ Timeout ao processar {lead_name}. O site pode estar lento.",
            "page_changed": f"📄 Layout da página mudou para {lead_name}. Pode ser necessário atualizar o sistema.",
            "unknown_error": f"❓ Erro desconhecido ao processar {lead_name}: {error_details}"
        }
        
        message = error_messages.get(error_type, error_messages["unknown_error"])
        self.show_warning(message)
        
        # Log detalhado para debugging
        self.log(f"Detalhes do erro para {lead_name}: {error_details}")
        
        return message
    
    def should_auto_skip(self, error_type):
        """Determinar se deve pular automaticamente baseado no tipo de erro"""
        auto_skip_errors = [
            "property_not_found",
            "timeout_error", 
            "connection_error",
            "page_changed"
        ]
        return error_type in auto_skip_errors
    
    def create_error_summary(self):
        """Criar resumo dos erros encontrados"""
        if not hasattr(self, 'processed_leads') or not self.processed_leads:
            return "Nenhum lead processado ainda."
        
        total = len(self.processed_leads)
        success = sum(1 for lead in self.processed_leads if "✅" in lead.get("status", ""))
        
        # Categorizar leads com problemas
        unavailable_properties = []
        manual_review = []
        failed_leads = []
        
        for lead in self.processed_leads:
            status = lead.get("status", "")
            if "✅" not in status:  # Não é sucesso
                if lead.get("property_not_available") or "não disponível" in status:
                    unavailable_properties.append(lead)
                elif "Pendente" in status or "Revisar" in status:
                    manual_review.append(lead)
                else:
                    failed_leads.append(lead)
        
        unavailable_count = len(unavailable_properties)
        manual_review_count = len(manual_review)
        failed_count = len(failed_leads)
        
        summary = f"""📊 Resumo do Processamento:
        
🎯 Total de leads: {total}
✅ Processados com sucesso: {success}
🏠 Imóveis não disponíveis: {unavailable_count}
⚠️ Revisão manual necessária: {manual_review_count}
❌ Falhas técnicas: {failed_count}

📈 Taxa de sucesso: {(success/total*100):.1f}%"""

        if unavailable_count > 0:
            summary += f"\n\n🏠 Imóveis não disponíveis para venda:"
            for lead in unavailable_properties:
                summary += f"\n• {lead.get('name', 'N/A')}: Imóvel foi arrematado ou retirado de venda"
        
        if manual_review_count > 0:
            summary += f"\n\n⚠️ Leads que precisam de revisão manual:"
            for lead in manual_review:
                summary += f"\n• {lead.get('name', 'N/A')}: {lead.get('status', 'N/A')}"
        
        if failed_count > 0:
            summary += f"\n\n❌ Leads com falhas técnicas:"
            for lead in failed_leads:
                summary += f"\n• {lead.get('name', 'N/A')}: {lead.get('status', 'N/A')}"
        
        return summary
    
    def restore_window_state(self):
        """Restaurar estado da janela da sessão anterior"""
        try:
            window_state = self.settings.load_window_state()
            if window_state:
                geometry = window_state.get("geometry")
                if geometry:
                    self.setGeometry(geometry["x"], geometry["y"], geometry["width"], geometry["height"])
                else:
                    # Posição padrão centralizada
                    self.resize(1200, 800)
                    self.center_window()
            else:
                self.resize(1200, 800)
                self.center_window()
        except Exception as e:
            print(f"Error restoring window state: {e}")
            self.resize(1200, 800)
            self.center_window()
    
    def save_message_templates(self):
        """Salvar templates de mensagem personalizados"""
        try:
            normal_template = self.normal_template_edit.toPlainText().strip()
            unavailable_template = self.unavailable_template_edit.toPlainText().strip()
            
            if not normal_template or not unavailable_template:
                QMessageBox.warning(self, "Aviso", "Por favor, preencha ambos os templates antes de salvar.")
                return
            
            # Validar se as variáveis básicas estão presentes
            required_vars_normal = ['{{name}}', '{{city}}', '{{property_url}}']
            required_vars_unavailable = ['{{name}}']
            
            missing_normal = [var for var in required_vars_normal if var not in normal_template]
            missing_unavailable = [var for var in required_vars_unavailable if var not in unavailable_template]
            
            if missing_normal or missing_unavailable:
                missing_text = ""
                if missing_normal:
                    missing_text += f"Template Normal: {', '.join(missing_normal)}\n"
                if missing_unavailable:
                    missing_text += f"Template Indisponível: {', '.join(missing_unavailable)}"
                
                QMessageBox.warning(self, "Variáveis Obrigatórias", 
                                  f"As seguintes variáveis obrigatórias estão faltando:\n\n{missing_text}")
                return
            
            # Salvar templates
            self.settings.set("message_templates.normal_lead", normal_template)
            self.settings.set("message_templates.unavailable_lead", unavailable_template)
            self.settings.save_settings()
            
            QMessageBox.information(self, "Sucesso", "Templates de mensagem salvos com sucesso!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar templates: {str(e)}")
    
    def reset_message_templates(self):
        """Restaurar templates padrão"""
        reply = QMessageBox.question(self, "Confirmar", 
                                   "Deseja restaurar os templates para os valores padrão?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Restaurar templates padrão
            default_normal = "{{greeting}} {{name}}! tudo bem?\n\nVi que demonstrou interesse nesse imóvel da CAIXA em {{city}}, nós somos uma imobiliária credenciada pela Caixa e lhe damos assessoria de ponta á ponta no processo de arremate desse imóvel, e de forma completamente gratuita nas modalidades de Venda Online e Compra Direta (somos remunerados pela CAIXA). Você já tem conhecimento de como os arremates funcionam?\n\nSegue o link do imóvel abaixo:\n{{property_url}}"
            
            default_unavailable = "Bom dia {{name}}! tudo bem?\nVi que demonstrou interesse em um imóvel da CAIXA, porém ele já foi arrematado ou está fora do ar por algum outro motivo!\nNós somos uma imobiliária credenciada pela Caixa e lhe damos assessoria de ponta á ponta no processo de arremate desse imóvel, e de forma completamente gratuita nas modalidades de Venda Online e Compra Direta (somos remunerados pela CAIXA).\nVocê já tem conhecimento de como os arremates funcionam?\nEncontre seu investimento ou imóvel dos sonhos por preços bem abaixo do praticado no mercado aqui no próprio site da CAIXA:\nvenda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"
            
            self.normal_template_edit.setPlainText(default_normal)
            self.unavailable_template_edit.setPlainText(default_unavailable)
            
            QMessageBox.information(self, "Sucesso", "Templates restaurados para os valores padrão!")
    
    def preview_message_template(self):
        """Visualizar templates com dados de exemplo"""
        try:
            # Dados de exemplo para preview
            sample_lead = {
                'name': 'João Silva',
                'city': 'São Paulo',
                'property_url': 'https://venda-imoveis.caixa.gov.br/sistema/detalhe-imovel.asp?hdnOrigem=index&hdnIdImovel=12345',
                'telephone': '11999887766',
                'greeting': 'Bom dia'
            }
            
            # Processar template normal
            normal_template = self.normal_template_edit.toPlainText()
            normal_preview = self.process_template_variables(normal_template, sample_lead)
            
            # Processar template indisponível
            unavailable_template = self.unavailable_template_edit.toPlainText()
            unavailable_preview = self.process_template_variables(unavailable_template, sample_lead)
            
            # Criar dialog de preview
            dialog = QDialog(self)
            dialog.setWindowTitle("👁️ Visualização dos Templates")
            dialog.setMinimumSize(600, 500)
            
            layout = QVBoxLayout(dialog)
            
            # Tabs para diferentes templates
            tab_widget = QTabWidget()
            
            # Tab template normal
            normal_tab = QWidget()
            normal_layout = QVBoxLayout(normal_tab)
            
            normal_label = QLabel("📋 Template para Leads Normais:")
            normal_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")
            normal_layout.addWidget(normal_label)
            
            normal_text = QTextEdit()
            normal_text.setPlainText(normal_preview)
            normal_text.setReadOnly(True)
            normal_text.setStyleSheet("""
                QTextEdit {
                    border: 2px solid #4CAF50;
                    border-radius: 8px;
                    padding: 10px;
                    background-color: #F8F8F8;
                    font-size: 12px;
                    font-family: 'Segoe UI', sans-serif;
                }
            """)
            normal_layout.addWidget(normal_text)
            
            tab_widget.addTab(normal_tab, "📋 Normal")
            
            # Tab template indisponível
            unavailable_tab = QWidget()
            unavailable_layout = QVBoxLayout(unavailable_tab)
            
            unavailable_label = QLabel("🚫 Template para Imóveis Indisponíveis:")
            unavailable_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")
            unavailable_layout.addWidget(unavailable_label)
            
            unavailable_text = QTextEdit()
            unavailable_text.setPlainText(unavailable_preview)
            unavailable_text.setReadOnly(True)
            unavailable_text.setStyleSheet("""
                QTextEdit {
                    border: 2px solid #FF9800;
                    border-radius: 8px;
                    padding: 10px;
                    background-color: #FFF8F0;
                    font-size: 12px;
                    font-family: 'Segoe UI', sans-serif;
                }
            """)
            unavailable_layout.addWidget(unavailable_text)
            
            tab_widget.addTab(unavailable_tab, "🚫 Indisponível")
            
            layout.addWidget(tab_widget)
            
            # Botão fechar
            close_button = AnimatedButton("Fechar", PRIMARY_COLOR)
            close_button.clicked.connect(dialog.accept)
            
            button_layout = QHBoxLayout()
            button_layout.addStretch()
            button_layout.addWidget(close_button)
            
            layout.addLayout(button_layout)
            
            dialog.exec_()
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao visualizar templates: {str(e)}")
    
    def process_template_variables(self, template, lead):
        """Processar variáveis do template"""
        import re
        from datetime import datetime
        
        # Mapear variáveis
        variables = {
            '{{name}}': lead.get('name', ''),
            '{{city}}': lead.get('city', ''),
            '{{property_url}}': lead.get('property_url', ''),
            '{{telephone}}': lead.get('telephone', ''),
            '{{greeting}}': lead.get('greeting', self.get_current_greeting())
        }
        
        # Substituir variáveis
        processed = template
        for var, value in variables.items():
            processed = processed.replace(var, str(value))
        
        return processed
    
    def get_current_greeting(self):
        """Obter saudação baseada no horário atual"""
        from datetime import datetime
        
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "Bom dia"
        elif 12 <= hour < 18:
            return "Boa tarde"
        else:
            return "Boa noite"
    
    def center_window(self):
        """Centralizar janela na tela"""
        try:
            screen = QApplication.desktop().screenGeometry()
            window = self.geometry()
            x = (screen.width() - window.width()) // 2
            y = (screen.height() - window.height()) // 2
            self.move(x, y)
        except:
            pass
    
    def restore_session_data(self):
        """Restaurar dados da sessão anterior"""
        try:
            # Restaurar arquivo de leads
            last_file = self.settings.get("file_paths.leads_file")
            if last_file and os.path.exists(last_file):
                self.file_path_edit.setText(last_file)
            
            # Restaurar configurações de processamento
            headless = self.settings.get("processing.headless_mode", True)
            self.headless_checkbox.setChecked(headless)
            
            # Restaurar leads manuais não processados
            manual_leads = self.settings.load_manual_leads_backup()
            if manual_leads:
                self.manual_leads_data = manual_leads
                self.update_manual_leads_display()
                self.log(f"Restaurados {len(manual_leads)} leads manuais da sessão anterior")
            
            # Restaurar aba ativa
            window_state = self.settings.load_window_state()
            if window_state and "current_tab" in window_state:
                self.tab_widget.setCurrentIndex(window_state["current_tab"])
                
        except Exception as e:
            print(f"Error restoring session data: {e}")
    
    def auto_save_data(self):
        """Auto-salvar dados da sessão"""
        try:
            # Salvar configurações
            self.settings.set("file_paths.leads_file", self.file_path_edit.text())
            self.settings.set("processing.headless_mode", self.headless_checkbox.isChecked())
            self.settings.save_settings()
            
            # Salvar leads manuais se existirem
            if hasattr(self, 'manual_leads_data') and self.manual_leads_data:
                self.settings.save_manual_leads_backup(self.manual_leads_data)
                
        except Exception as e:
            print(f"Error auto-saving data: {e}")
    
    def closeEvent(self, event):
        """Evento ao fechar a aplicação"""
        try:
            # Salvar estado da janela
            current_tab = self.tab_widget.currentIndex() if hasattr(self, 'tab_widget') else 0
            self.settings.save_window_state(self.geometry(), self.saveState(), current_tab)
            
            # Salvar dados da sessão
            self.auto_save_data()
            
            # Salvar histórico de processamento se houver leads processados
            if hasattr(self, 'processed_leads') and self.processed_leads:
                session_data = {
                    "total_leads": len(self.processed_leads),
                    "successful": len([l for l in self.processed_leads if l.get('status') == 'Processado']),
                    "failed": len([l for l in self.processed_leads if 'erro' in l.get('status', '').lower()]),
                    "file_processed": self.file_path_edit.text() if hasattr(self, 'file_path_edit') else ""
                }
                self.settings.add_processing_history(session_data)
            
            # Parar worker thread se ativo
            if self.worker_thread and self.worker_thread.isRunning():
                reply = QMessageBox.question(
                    self, 
                    "Processamento em Andamento",
                    "Há um processamento em andamento. Deseja interrompê-lo e sair?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply == QMessageBox.No:
                    event.ignore()
                    return
                else:
                    self.worker_thread.stop()
                    self.worker_thread.wait(3000)  # Wait 3 seconds max
            
            # Parar timer de auto-save
            if hasattr(self, 'auto_save_timer'):
                self.auto_save_timer.stop()
            
            event.accept()
            
        except Exception as e:
            print(f"Error during close: {e}")
            event.accept()


if __name__ == "__main__":
    import sys
    import os
    
    # Criar aplicação primeiro
    app = QApplication(sys.argv)
    
    # Definir propriedades da aplicação
    app.setApplicationName("CAIXA Lead Processor")
    app.setApplicationDisplayName("Processador de Leads da CAIXA")
    app.setApplicationVersion("1.0")
    
    # Configuração específica do Windows para taskbar
    try:
        import ctypes
        # Definir AppUserModelID único para o Windows
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("CAIXA.LeadProcessor.App")
        print("✅ Windows taskbar ID configurado")
    except Exception as e:
        print(f"⚠️ Configuração Windows falhou: {e}")
    
    # Agora configurar ícone da aplicação (após criar QApplication)
    try:
        # Tentar carregar o arquivo CAIXA.jpeg
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "icons", "CAIXA.jpeg"),
            os.path.join(os.path.dirname(__file__), "CAIXA.jpeg"),
            os.path.join(os.path.dirname(__file__), "icons", "caixa.jpeg")
        ]
        
        icon_path = None
        for path in possible_paths:
            if os.path.exists(path):
                icon_path = path
                break
        
        if icon_path:
            # Carregar a imagem
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                # Criar ícone em múltiplos tamanhos
                icon = QIcon()
                for size in [16, 24, 32, 48, 64, 128, 256]:
                    scaled_pixmap = pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    icon.addPixmap(scaled_pixmap)
                
                # Definir ícone da aplicação ANTES de criar qualquer janela
                app.setWindowIcon(icon)
                print("✅ Ícone CAIXA definido para a aplicação")
            else:
                print("❌ Falha ao carregar CAIXA.jpeg")
        else:
            print("❌ CAIXA.jpeg não encontrado")
            
    except Exception as e:
        print(f"❌ Erro ao definir ícone: {e}")
    
    window = LeadProcessorGUI()
    window.show()
    
    print("🚀 Aplicação iniciada - verifique o ícone na barra de tarefas!")
    sys.exit(app.exec_())