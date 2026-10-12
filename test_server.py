"""
Teste de integridade do servidor web e rotas da API.
"""

from server import app

client = app.test_client()

print("[1] Testando rota GET /...")
res_index = client.get("/")
assert res_index.status_code == 200, f"Falha no index: {res_index.status_code}"
assert "Banda Litúrgica" in res_index.text, "Index não contém título esperado"
print("✓ Rota GET / retornou 200 OK com template HTML renderizado!")

print("\n[2] Testando rota GET /api/status...")
res_status = client.get("/api/status")
assert res_status.status_code == 200
data_status = res_status.get_json()
print("✓ Status do Servidor:", data_status)

print("\n[3] Testando rota POST /api/compose...")
briefing_data = {
    "theme": "A Graça que Salva e Sustenta",
    "biblical_reference": "Efésios 2:8-10 e Romanos 8:38-39",
    "musical_style_hint": "Modern Worship congregacional solene",
    "tempo_hint": "Lento para médio (72 BPM)",
    "vocal_preference": "Voz masculina emotiva"
}
res_compose = client.post("/api/compose", json=briefing_data)
assert res_compose.status_code == 200
data_compose = res_compose.get_json()
assert data_compose["success"] is True
print("✓ Composição gerada com sucesso via API!")
print("  - Título:", data_compose["suno_package"]["song_title"])
print("  - Style Prompt:", data_compose["suno_package"]["style_of_music"])
print("  - Nota do Auditor:", data_compose["audit"]["score"])

print("\n🎉 TODOS OS TESTES DO SERVIDOR PASSARAM COM SUCESSO TOTAL!")
