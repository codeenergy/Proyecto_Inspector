"""
Script de demostración para explorar dominios
Uso: python explore_demo.py https://ejemplo.com
"""
import asyncio
import sys
import json
import os

# Fix encoding para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from modules.web_explorer import explore_website


async def main():
    if len(sys.argv) < 2:
        print("ERROR: Debes proporcionar una URL")
        print("\nUso:")
        print("  python explore_demo.py https://ejemplo.com")
        print("\nEjemplos:")
        print("  python explore_demo.py https://amazon.com")
        print("  python explore_demo.py https://mercadolibre.com")
        print("  python explore_demo.py https://tu-tienda.com")
        sys.exit(1)

    url = sys.argv[1]

    print("=" * 80)
    print("Ad-Inspector Bot - Explorador Web")
    print("=" * 80)
    print(f"\nURL a explorar: {url}")
    print(f"Profundidad maxima: 2 niveles")
    print(f"Maximo de paginas: 30")
    print(f"\nIniciando exploracion (esto puede tomar varios minutos)...\n")

    # Ejecutar exploración
    result = await explore_website(
        url=url,
        max_depth=2,
        max_pages=30
    )

    # Mostrar resultados
    print("\n" + "=" * 80)
    print("EXPLORACION COMPLETADA")
    print("=" * 80)
    print(f"\nEstadisticas:")
    print(f"  - Paginas visitadas: {result['total_pages_visited']}")
    print(f"  - Botones encontrados: {result['total_buttons_clicked']}")
    print(f"  - Enlaces seguidos: {result['total_links_followed']}")
    print(f"  - ANUNCIOS encontrados: {result['total_ads_found']}")
    print(f"  - Formularios detectados: {result['total_forms_found']}")

    print(f"\nPaginas exploradas:")
    for i, page in enumerate(result['sitemap'][:10], 1):
        print(f"  {i}. {page}")

    if len(result['sitemap']) > 10:
        print(f"  ... y {len(result['sitemap']) - 10} paginas mas")

    # Guardar resultados en JSON
    output_file = "exploration_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nResultados guardados en: {output_file}")
    print("\nExploracion completada con exito!")


if __name__ == "__main__":
    asyncio.run(main())
