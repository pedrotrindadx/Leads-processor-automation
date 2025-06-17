"""
CAIXA Lead Processor - Settings Manager
Manages application settings, preferences, and data persistence
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path

class AppSettings:
    """Manage application settings and data persistence"""
    
    def __init__(self):
        self.app_dir = Path(__file__).parent
        self.config_dir = self.app_dir / "config"
        self.data_dir = self.app_dir / "data"
        self.logs_dir = self.app_dir / "logs"
        self.cache_dir = self.app_dir / "cache"
        self.temp_dir = self.app_dir / "temp"
        
        # Ensure directories exist
        for directory in [self.config_dir, self.data_dir, self.logs_dir, self.cache_dir, self.temp_dir]:
            directory.mkdir(exist_ok=True)
        
        self.settings_file = self.config_dir / "settings.json"
        self.window_state_file = self.config_dir / "window_state.json"
        self.manual_leads_file = self.data_dir / "manual_leads_backup.json"
        self.processing_history_file = self.data_dir / "processing_history.json"
        
        # Default settings
        self.default_settings = {
            "app_version": "1.0.0",
            "last_opened": None,
            "file_paths": {
                "leads_file": str(self.app_dir / "leads.txt"),
                "last_export_dir": str(self.data_dir)
            },
            "processing": {
                "headless_mode": True,
                "auto_save_interval": 300,  # 5 minutes
                "max_log_files": 10,
                "max_history_entries": 100
            },
            "ui": {
                "theme": "default",
                "auto_switch_tabs": True,
                "show_confirmations": True,
                "animation_enabled": True
            },
            "whatsapp": {
                "prefer_app_over_web": True,
                "auto_advance_after_send": True
            },
            "message_templates": {
                "normal_lead": "{{greeting}} {{name}}! tudo bem?\n\nVi que demonstrou interesse nesse imóvel da CAIXA em {{city}}, nós somos uma imobiliária credenciada pela Caixa e lhe damos assessoria de ponta á ponta no processo de arremate desse imóvel, e de forma completamente gratuita nas modalidades de Venda Online e Compra Direta (somos remunerados pela CAIXA). Você já tem conhecimento de como os arremates funcionam?\n\nSegue o link do imóvel abaixo:\n{{property_url}}",
                "unavailable_lead": "Bom dia {{name}}! tudo bem?\nVi que demonstrou interesse em um imóvel da CAIXA, porém ele já foi arrematado ou está fora do ar por algum outro motivo!\nNós somos uma imobiliária credenciada pela Caixa e lhe damos assessoria de ponta á ponta no processo de arremate desse imóvel, e de forma completamente gratuita nas modalidades de Venda Online e Compra Direta (somos remunerados pela CAIXA).\nVocê já tem conhecimento de como os arremates funcionam?\nEncontre seu investimento ou imóvel dos sonhos por preços bem abaixo do praticado no mercado aqui no próprio site da CAIXA:\nvenda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"
            }
        }
        
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from file or create default"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                # Merge with defaults to handle new settings
                settings = self.default_settings.copy()
                self._deep_update(settings, loaded_settings)
                return settings
            else:
                return self.default_settings.copy()
        except Exception as e:
            print(f"Error loading settings: {e}")
            return self.default_settings.copy()
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            self.settings["last_opened"] = datetime.now().isoformat()
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get(self, key_path, default=None):
        """Get setting value using dot notation (e.g., 'ui.theme')"""
        try:
            keys = key_path.split('.')
            value = self.settings
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path, value):
        """Set setting value using dot notation"""
        try:
            keys = key_path.split('.')
            current = self.settings
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            current[keys[-1]] = value
            return True
        except Exception as e:
            print(f"Error setting value: {e}")
            return False
    
    def save_window_state(self, geometry, state, tab_index=0):
        """Save window geometry and state"""
        try:
            window_data = {
                "geometry": {
                    "x": geometry.x(),
                    "y": geometry.y(),
                    "width": geometry.width(),
                    "height": geometry.height()
                },
                "state": state.toHex().data().decode() if state else None,
                "current_tab": tab_index,
                "timestamp": datetime.now().isoformat()
            }
            
            with open(self.window_state_file, 'w', encoding='utf-8') as f:
                json.dump(window_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving window state: {e}")
            return False
    
    def load_window_state(self):
        """Load window geometry and state"""
        try:
            if self.window_state_file.exists():
                with open(self.window_state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error loading window state: {e}")
            return None
    
    def save_manual_leads_backup(self, leads_data):
        """Save manual leads as backup"""
        try:
            if not leads_data:
                return True
            
            backup_data = {
                "leads": leads_data,
                "timestamp": datetime.now().isoformat(),
                "count": len(leads_data)
            }
            
            with open(self.manual_leads_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving manual leads backup: {e}")
            return False
    
    def load_manual_leads_backup(self):
        """Load manual leads backup"""
        try:
            if self.manual_leads_file.exists():
                with open(self.manual_leads_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data.get("leads", [])
            return []
        except Exception as e:
            print(f"Error loading manual leads backup: {e}")
            return []
    
    def add_processing_history(self, session_data):
        """Add processing session to history"""
        try:
            history = self.load_processing_history()
            
            # Add new session
            session_data["timestamp"] = datetime.now().isoformat()
            history.append(session_data)
            
            # Keep only max entries
            max_entries = self.get("processing.max_history_entries", 100)
            history = history[-max_entries:]
            
            with open(self.processing_history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving processing history: {e}")
            return False
    
    def load_processing_history(self):
        """Load processing history"""
        try:
            if self.processing_history_file.exists():
                with open(self.processing_history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading processing history: {e}")
            return []
    
    def clear_cache(self):
        """Clear all cache files"""
        try:
            cleared_files = 0
            
            # Clear cache directory
            if self.cache_dir.exists():
                for file in self.cache_dir.glob("*"):
                    if file.is_file():
                        file.unlink()
                        cleared_files += 1
                    elif file.is_dir():
                        shutil.rmtree(file)
                        cleared_files += 1
            
            # Clear temp directory
            if self.temp_dir.exists():
                for file in self.temp_dir.glob("*"):
                    if file.is_file():
                        file.unlink()
                        cleared_files += 1
                    elif file.is_dir():
                        shutil.rmtree(file)
                        cleared_files += 1
            
            # Clear old log files (keep last 10)
            if self.logs_dir.exists():
                log_files = sorted(self.logs_dir.glob("*.log"), key=lambda x: x.stat().st_mtime)
                max_logs = self.get("processing.max_log_files", 10)
                for log_file in log_files[:-max_logs]:
                    log_file.unlink()
                    cleared_files += 1
            
            # Clear browser cache if exists
            browser_cache_dirs = [
                self.cache_dir / "selenium",
                self.cache_dir / "chromedriver",
                Path.home() / ".wdm" / "drivers"
            ]
            
            for cache_dir in browser_cache_dirs:
                if cache_dir.exists():
                    try:
                        shutil.rmtree(cache_dir)
                        cleared_files += 1
                    except:
                        pass
            
            return cleared_files
        except Exception as e:
            print(f"Error clearing cache: {e}")
            return 0
    
    def get_app_info(self):
        """Get application information"""
        return {
            "version": self.get("app_version"),
            "last_opened": self.get("last_opened"),
            "config_dir": str(self.config_dir),
            "data_dir": str(self.data_dir),
            "logs_dir": str(self.logs_dir),
            "cache_dir": str(self.cache_dir),
            "settings_file": str(self.settings_file),
            "total_history_entries": len(self.load_processing_history()),
            "manual_leads_backup": len(self.load_manual_leads_backup())
        }
    
    def reset_to_defaults(self):
        """Reset all settings to default values"""
        try:
            self.settings = self.default_settings.copy()
            self.save_settings()
            return True
        except Exception as e:
            print(f"Error resetting settings: {e}")
            return False
    
    def export_data(self, export_path):
        """Export all user data to a zip file"""
        try:
            import zipfile
            
            with zipfile.ZipFile(export_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add config files
                for file in self.config_dir.glob("*.json"):
                    zipf.write(file, f"config/{file.name}")
                
                # Add data files
                for file in self.data_dir.glob("*.json"):
                    zipf.write(file, f"data/{file.name}")
                
                # Add recent logs
                log_files = sorted(self.logs_dir.glob("*.log"), key=lambda x: x.stat().st_mtime)
                for log_file in log_files[-5:]:  # Last 5 log files
                    zipf.write(log_file, f"logs/{log_file.name}")
                
                # Add leads.txt if exists
                leads_file = self.app_dir / "leads.txt"
                if leads_file.exists():
                    zipf.write(leads_file, "leads.txt")
            
            return True
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False
    
    def _deep_update(self, base_dict, update_dict):
        """Deep update dictionary"""
        for key, value in update_dict.items():
            if isinstance(value, dict) and key in base_dict and isinstance(base_dict[key], dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value