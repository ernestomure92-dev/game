#!/usr/bin/env python3
"""
🦝 RaccoonDev - Tu mapache GitHub mascota
Lógica de estados, interacciones y evolución
"""

import json
import os
import argparse
from datetime import datetime, timedelta
from pathlib import Path

class RaccoonDev:
    def __init__(self):
        self.state_file = Path("data/pet-state.json")
        self.state = self.load_state()
        
    def load_state(self):
        """Carga o inicializa el estado del mapache"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        
        # Estado inicial del bebé mapache
        return {
            "name": "RaccoonDev",
            "species": "raccoon",
            "level": 1,
            "xp": 0,
            "stats": {
                "energy": 80,
                "hunger": 20,
                "happiness": 70,
                "coding_mojo": 50,
                "stress": 0
            },
            "mood": "curious",
            "last_update": datetime.now().isoformat(),
            "total_interactions": 0,
            "commits_fed": 0,
            "evolution_stage": "baby",  # baby -> junior -> senior -> tech_lead
            "inventory": {
                "coffee": 3,
                "pizza": 2,
                "bugs_fixed": 0
            },
            "achievements": []
        }
    
    def save_state(self):
        """Guarda el estado actual"""
        self.state_file.parent.mkdir(exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def update_natural_decay(self):
        """Actualiza degradación natural cada 4 horas"""
        last = datetime.fromisoformat(self.state["last_update"])
        now = datetime.now()
        hours_passed = (now - last).total_seconds() / 3600
        
        # Degradación por hora
        decay_rates = {
            "energy": -2,
            "hunger": +3,
            "happiness": -1,
            "coding_mojo": -1
        }
        
        for stat, rate in decay_rates.items():
            self.state["stats"][stat] = max(0, min(100, 
                self.state["stats"][stat] + (rate * hours_passed)
            ))
        
        self.state["last_update"] = now.isoformat()
        self.update_mood()
        
    def update_mood(self):
        """Determina el mood basado en stats"""
        stats = self.state["stats"]
        
        if stats["energy"] < 20:
            self.state["mood"] = "exhausted"
        elif stats["hunger"] > 80:
            self.state["mood"] = "starving"
        elif stats["stress"] > 70:
            self.state["mood"] = "burned_out"
        elif stats["coding_mojo"] > 80 and stats["energy"] > 60:
            self.state["mood"] = "flow_state"
        elif stats["happiness"] > 80:
            self.state["mood"] = "happy"
        elif stats["energy"] > 70:
            self.state["mood"] = "focused"
        else:
            self.state["mood"] = "chill"
    
    def feed(self, food_type):
        """Alimentar al mapache"""
        effects = {
            "pizza": {"hunger": -30, "energy": +10, "happiness": +5, "msg": "🍕 ¡Pizza party!"},
            "sushi": {"hunger": -25, "energy": +15, "coding_mojo": +5, "msg": "🍣 Sushi premium"},
            "coffee": {"energy": +25, "coding_mojo": +20, "hunger": -5, "stress": +10, 
                      "msg": "☕ ¡Café para el crunch!"},
            "taco": {"hunger": -20, "happiness": +15, "energy": +5, "msg": "🌮 Taco Tuesday!"},
            "salad": {"hunger": -15, "energy": +5, "stress": -10, "msg": "🥗 Día saludable"},
            "commit": {"hunger": -10, "happiness": +5, "coding_mojo": +10, 
                      "msg": "🍴 Se alimentó de tu commit"}
        }
        
        if food_type not in effects:
            return False, f"❌ No me gusta {food_type}. Prueba: pizza, sushi, coffee, taco, salad"
        
        effect = effects[food_type]
        
        # Aplicar efectos
        for stat, value in effect.items():
            if stat != "msg":
                current = self.state["stats"].get(stat, 0)
                self.state["stats"][stat] = max(0, min(100, current + value))
        
        self.state["total_interactions"] += 1
        if food_type == "commit":
            self.state["commits_fed"] += 1
        
        self.add_xp(10)
        self.update_mood()
        
        return True, effect["msg"]
    
    def play(self, activity):
        """Jugar con el mapache"""
        activities = {
            "debug": {"happiness": +15, "coding_mojo": +10, "energy": -10, 
                     "msg": "🐛 ¡Debuggeando juntos! Bugs temen nuestra unión"},
            "refactor": {"coding_mojo": +20, "stress": +5, "energy": -15,
                        "msg": "♻️ Refactor épico. Código limpio, alma limpia"},
            "deploy": {"happiness": +20, "stress": +20, "coding_mojo": +5,
                      "msg": "🚀 ¡Deploy! (Esperando que no rompa producción...)"},
            "pet": {"happiness": +10, "stress": -15, "energy": -5,
                   "msg": "🤗 *Ronronea en binario*"},
            "code_review": {"coding_mojo": +15, "happiness": -5, "stress": +10,
                           "msg": "👀 Code review... encontró 5 issues pero aprendió mucho"}
        }
        
        if activity not in activities:
            return False, f"❌ No sé cómo '{activity}'. Opciones: debug, refactor, deploy, pet, code_review"
        
        effect = activities[activity]
        
        # Verificar energía
        if self.state["stats"]["energy"] < 15:
            return False, "😴 Estoy muy cansado... necesito dormir primero"
        
        for stat, value in effect.items():
            if stat != "msg":
                current = self.state["stats"].get(stat, 0)
                self.state["stats"][stat] = max(0, min(100, current + value))
        
        self.state["total_interactions"] += 1
        self.add_xp(15)
        self.update_mood()
        
        return True, effect["msg"]
    
    def sleep(self):
        """Dormir (recuperación completa)"""
        if self.state["stats"]["energy"] > 80:
            return False, "😳 ¡No tengo sueño! Energía al " + str(int(self.state["stats"]["energy"])) + "%"
        
        self.state["stats"]["energy"] = 100
        self.state["stats"]["stress"] = max(0, self.state["stats"]["stress"] - 30)
        self.state["stats"]["hunger"] = min(100, self.state["stats"]["hunger"] + 10)
        self.state["last_sleep"] = datetime.now().isoformat()
        
        self.update_mood()
        self.add_xp(5)
        
        return True, "💤 ¡ZZZ... soñando con código limpio y commits verdes!"
    
    def process_commit(self, commit_msg):
        """Procesar un push/commit como alimento"""
        bonus = 0
        if "fix" in commit_msg.lower() or "bug" in commit_msg.lower():
            bonus = 10
            self.state["inventory"]["bugs_fixed"] += 1
            msg = "🐛 ¡Commit de bugfix! +10 bonus"
        elif "feat" in commit_msg.lower() or "add" in commit_msg.lower():
            bonus = 15
            msg = "✨ ¡Nueva feature! +15 bonus"
        elif "refactor" in commit_msg.lower():
            bonus = 20
            msg = "♻️ ¡Refactor heroico! +20 bonus"
        else:
            msg = "📝 Commit recibido"
        
        success, feed_msg = self.feed("commit")
        self.add_xp(10 + bonus)
        
        return f"{msg}\n{feed_msg} (+{bonus} XP)"
    
    def add_xp(self, amount):
        """Añadir experiencia y verificar level up"""
        self.state["xp"] += amount
        
        # Sistema de niveles
        levels = [0, 100, 250, 500, 1000, 1500, 2500, 4000, 6000, 10000]
        new_level = 1
        for i, xp_needed in enumerate(levels):
            if self.state["xp"] >= xp_needed:
                new_level = i + 1
        
        if new_level > self.state["level"]:
            self.state["level"] = new_level
            # Evoluciones
            if new_level >= 15:
                self.state["evolution_stage"] = "tech_lead"
            elif new_level >= 10:
                self.state["evolution_stage"] = "senior"
            elif new_level >= 5:
                self.state["evolution_stage"] = "junior"
            
            return f"🎉 ¡LEVEL UP! Ahora soy nivel {new_level} ({self.state['evolution_stage']})!"
        return None
    
    def get_ascii(self):
        """Obtener representación ASCII según estado"""
        mood = self.state["mood"]
        stage = self.state["evolution_stage"]
        
        # Sprites base por evolución
        sprites = {
            "baby": {
                "curious": r"""
    🦝
  <(o_o)>
  /|   |\
   |___|
  /     \
  """,
                "focused": r"""
    🦝
  <(o_o)>⌨️
  /|   |\
   |___|
  /     \
  """,
                "exhausted": r"""
    😴
  <(-_-)>
  /|   |\
   |___|
  /     \
  """,
                "flow_state": r"""
    🦝⚡
  <(o_o)>⌨️
  /|   |\
   |___|
  /     \
  """,
                "happy": r"""
    🦝✨
  <(^_^)>
  /|   |\
   |___|
  /     \
  """
            },
            "junior": {
                "focused": r"""
      🦝
    <(o_o)>⌨️  💻
   /| 👔 |\
    |____|
   /      \
  /   🐛   \
  """,
                "flow_state": r"""
      🦝☕
    <(o_o)>⌨️  🚀
   /| 👔 |\
    |____|
   /      \
  /  🔥🔥  \
  """
            },
            "senior": {
                "focused": r"""
       🦝
     <(o_o)>⌨️  🖥️🖥️🖥️
    /| 🎧 |\
     |____|
    /      \
   /  ☕ ☕   \
  /____________\
  """,
                "flow_state": r"""
       🦝👑
     <(o_o)>⌨️  🚀🚀
    /| 🎧 |\
     |____|
    /      \
   /  🔥🔥🔥  \
  /____________\
  """
            },
            "tech_lead": {
                "focused": r"""
        🦝
      <(o_o)>⌨️  🏢 Cloud
     /| 👓 🎧 |\
      |______|
     /        \
    /  ☕ ☕ ☕   \
   /______________\
   📊 Dashboard  🐋 Docker
  """,
                "flow_state": r"""
        🦝👔
      <(o_o)>⌨️  🌍 Global
     /| 👓 🎧 |\
      |______|
     /        \
    /  🔥🔥🔥🔥  \
   /______________\
   🚀 Kubernetes  ☁️ AWS
  """
            }
        }
        
        # Default fallback
        if stage not in sprites:
            stage = "baby"
        if mood not in sprites[stage]:
            mood = "curious"
            
        return sprites[stage][mood]
    
    def get_status_badge(self):
        """Generar badges de estado para README"""
        stats = self.state["stats"]
        mood = self.state["mood"]
        
        # Color según salud general
        health = (stats["energy"] + (100 - stats["hunger"]) + stats["happiness"]) / 3
        
        if health > 80:
            color = "brightgreen"
            status = "Thriving"
        elif health > 60:
            color = "green"
            status = "Good"
        elif health > 40:
            color = "yellow"
            status = "Okay"
        else:
            color = "red"
            status = "Needs Care"
        
        return {
            "main": f"https://img.shields.io/badge/RaccoonDev-{status}-{color}?logo=github",
            "energy": f"https://img.shields.io/badge/Energy-{int(stats['energy'])}%25-{self._stat_color(stats['energy'])}",
            "hunger": f"https://img.shields.io/badge/Hunger-{int(stats['hunger'])}%25-{self._stat_color(100-stats['hunger'])}",
            "happiness": f"https://img.shields.io/badge/Happiness-{int(stats['happiness'])}%25-{self._stat_color(stats['happiness'])}",
            "mojo": f"https://img.shields.io/badge/Coding_Mojo-{int(stats['coding_mojo'])}%25-{self._stat_color(stats['coding_mojo'])}",
            "level": f"https://img.shields.io/badge/Level-{self.state['level']}-blue"
        }
    
    def _stat_color(self, value):
        if value > 80: return "brightgreen"
        if value > 60: return "green"
        if value > 40: return "yellow"
        if value > 20: return "orange"
        return "red"

def main():
    parser = argparse.ArgumentParser(description="🦝 RaccoonDev Bot")
    parser.add_argument("--event", required=True)
    parser.add_argument("--action", default="auto")
    parser.add_argument("--issue-number", default="0")
    parser.add_argument("--issue-body", default="")
    parser.add_argument("--commit-message", default="")
    
    args = parser.parse_args()
    
    raccoon = RaccoonDev()
    response = ""
    commit_msg = "🦝 Update: estado natural"
    
    try:
        # Procesar eventos
        if args.event == "schedule":
            raccoon.update_natural_decay()
            response = "⏰ Actualización automática completada"
            
        elif args.event == "push":
            if args.commit_message:
                result = raccoon.process_commit(args.commit_message)
                response = f"🍴 Commit detectado!\n{result}"
                commit_msg = f"🦝 [Auto] Fed by commit: {args.commit_message[:30]}..."
            else:
                raccoon.update_natural_decay()
                
        elif args.event == "issues":
            body = args.issue_body.lower()
            
            # Parsear comandos
            if "/feed" in body:
                food = body.replace("/feed", "").strip().split()[0] if len(body.replace("/feed", "").strip().split()) > 0 else "pizza"
                success, msg = raccoon.feed(food)
                response = msg if success else f"❌ {msg}"
                commit_msg = f"🦝 [Feed] Ate {food}"
                
            elif "/play" in body:
                activity = body.replace("/play", "").strip().split()[0] if len(body.replace("/play", "").strip().split()) > 0 else "pet"
                success, msg = raccoon.play(activity)
                response = msg if success else f"❌ {msg}"
                commit_msg = f"🦝 [Play] {activity}"
                
            elif "/sleep" in body:
                success, msg = raccoon.sleep()
                response = msg if success else f"❌ {msg}"
                commit_msg = "🦝 [Sleep] ZZZ..."
                
            elif "/status" in body or "/stats" in body:
                stats = raccoon.state["stats"]
                response = f"""
📊 **Estado de {raccoon.state['name']}**

🍕 Hambre: {int(stats['hunger'])}/100
⚡ Energía: {int(stats['energy'])}/100
😊 Felicidad: {int(stats['happiness'])}/100
💻 Coding Mojo: {int(stats['coding_mojo'])}/100
😰 Estrés: {int(stats['stress'])}/100

🎭 Mood: **{raccoon.state['mood']}**
⭐ Nivel: {raccoon.state['level']} ({raccoon.state['evolution_stage']})
📈 XP: {raccoon.state['xp']}
🍴 Commits alimentados: {raccoon.state['commits_fed']}
"""
                commit_msg = "🦝 [Status] Check"
                
            else:
                response = """
🦝 **¡Hola! Soy RaccoonDev**

Comandos disponibles:
- `/feed [pizza|sushi|coffee|taco|salad]` - Alimentarme
- `/play [debug|refactor|deploy|pet|code_review]` - Jugar
- `/sleep` - Dormir (recupera energía)
- `/status` - Ver mis stats

También me alimento automáticamente cuando haces commits! 🍴
"""
                commit_msg = "🦝 [Help] Command list"
        
        # Guardar estado
        raccoon.save_state()
        
        # Output para GitHub Actions
        print(f"::set-output name=response::{response}")
        print(f"::set-output name=commit_message::{commit_msg}")
        print(f"COMMIT_MSG={commit_msg}")
        
    except Exception as e:
        print(f"::error::Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
