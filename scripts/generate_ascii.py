#!/usr/bin/env python3
"""
Generador del README.md con el dashboard del mapache
"""

import json
from datetime import datetime
from pathlib import Path

def generate_readme():
    # Cargar estado
    state_file = Path("data/pet-state.json")
    if not state_file.exists():
        print("No state file found")
        return
    
    with open(state_file, 'r') as f:
        state = json.load(f)
    
    # Cargar sprites según estado
    mood = state["mood"]
    stage = state["evolution_stage"]
    
    # ASCII art según estado (simplificado para README)
    ascii_art = get_ascii_by_mood(mood, stage)
    
    # Badges
    stats = state["stats"]
    health = (stats["energy"] + (100 - stats["hunger"]) + stats["happiness"]) / 3
    
    if health > 80:
        status_color = "brightgreen"
        status_text = "Thriving"
    elif health > 60:
        status_color = "green"
        status_text = "Good"
    elif health > 40:
        status_color = "yellow"
        status_text = "Okay"
    else:
        status_color = "red"
        status_text = "Needs Care"
    
    # Emojis de estado
    mood_emoji = {
        "curious": "🤔",
        "focused": "🎯",
        "exhausted": "😴",
        "starving": "🤤",
        "burned_out": "😵",
        "flow_state": "⚡",
        "happy": "😊",
        "chill": "😌"
    }.get(mood, "🦝")
    
    # Generar README
    readme = f"""# 🦝 {state['name']} - Tu Mapache Developer

![Status](https://img.shields.io/badge/Status-{status_text}-{status_color}?logo=github)
![Level](https://img.shields.io/badge/Level-{state['level']}-blue)
![Stage](https://img.shields.io/badge/Evolution-{state['evolution_stage']}-purple)

<div align="center">

{ascii_art}

**{mood_emoji} Current Mood: `{mood}`**

</div>

---

## 📊 Stats en Tiempo Real

| Stat | Valor | Barra |
|------|-------|-------|
| ⚡ **Energía** | {int(stats['energy'])}% | {generate_bar(stats['energy'])} |
| 🍕 **Hambre** | {int(stats['hunger'])}% | {generate_bar(100 - stats['hunger'], inverse=True)} |
| 😊 **Felicidad** | {int(stats['happiness'])}% | {generate_bar(stats['happiness'])} |
| 💻 **Coding Mojo** | {int(stats['coding_mojo'])}% | {generate_bar(stats['coding_mojo'])} |
| 😰 **Estrés** | {int(stats['stress'])}% | {generate_bar(stats['stress'])} |

---

## 🎮 Interactúa Conmigo

Abre un [Issue](../../issues/new) con estos comandos:

### 🍴 Alimentar
