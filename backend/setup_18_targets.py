"""
Script para crear 18 targets optimizados (6 por cada dominio)
Ejecutar UNA VEZ para poblar la base de datos
"""
import sqlite3
from pathlib import Path

# Configuración de los 3 dominios
DOMAINS = [
    "https://cofreprompt.com",
    "https://scoopnewspaper.com",
    "https://atlascine.com"
]

# Configuraciones variadas para cada dominio (6 targets por dominio)
TARGET_CONFIGS = [
    {"pageviews": 6, "click_prob": 0.45},
    {"pageviews": 8, "click_prob": 0.55},
    {"pageviews": 10, "click_prob": 0.60},
    {"pageviews": 12, "click_prob": 0.65},
    {"pageviews": 14, "click_prob": 0.70},
    {"pageviews": 15, "click_prob": 0.72},
]

def setup_targets():
    """Crear los 18 targets en la base de datos"""
    db_path = Path(__file__).parent / "inspector.db"

    if not db_path.exists():
        print("❌ Base de datos no encontrada. Ejecuta primero: python init_database.py")
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Limpiar targets antiguos (excepto example.com si quieres mantenerlo)
    print("🗑️  Limpiando targets antiguos...")
    cursor.execute("DELETE FROM bot_targets WHERE url LIKE '%example.com%'")

    # Crear los 18 targets
    print("\n📝 Creando 18 targets optimizados...")
    count = 0

    for domain in DOMAINS:
        print(f"\n🌐 Dominio: {domain}")

        for i, config in enumerate(TARGET_CONFIGS, 1):
            cursor.execute("""
                INSERT INTO bot_targets
                (url, enabled, target_pageviews, min_duration_seconds, ad_click_probability, viewport)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                domain,
                1,  # enabled
                config["pageviews"],
                60,  # min_duration_seconds
                config["click_prob"],
                '{"width": 1920, "height": 1080}'
            ))
            count += 1
            print(f"  ✅ Target {i}/6: {config['pageviews']} views, {int(config['click_prob']*100)}% click")

    conn.commit()

    # Verificar
    cursor.execute("SELECT COUNT(*) FROM bot_targets WHERE enabled=1")
    total = cursor.fetchone()[0]

    print(f"\n✅ Total de targets activos: {total}")

    # Mostrar resumen por dominio
    print("\n📊 Resumen por dominio:")
    for domain in DOMAINS:
        cursor.execute("SELECT COUNT(*) FROM bot_targets WHERE url=? AND enabled=1", (domain,))
        count = cursor.fetchone()[0]
        print(f"  {domain}: {count} targets")

    conn.close()
    return True

if __name__ == "__main__":
    print("🚀 Setup de 18 Targets Optimizados\n")
    print("=" * 60)

    try:
        if setup_targets():
            print("\n" + "=" * 60)
            print("🎉 ¡18 targets creados exitosamente!")
            print("\nAhora puedes:")
            print("  1. Reiniciar el servidor backend")
            print("  2. El bot ejecutará sesiones en los 18 targets")
            print("  3. Verificar en el dashboard")
        else:
            print("\n❌ Error al crear targets")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
