"""CA-2: casa do próprio tema e `mencionar` não avisam; sem --temas, nenhum aviso."""


def test_CA2_sem_aviso(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    r = livro('validar-briefing', 'teste', 'briefing-tema1.md', '--temas', 'temas-ok.md')
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        'ok: 2 momentos, 2 passagens, 0 citações, 0 dados da web\n'
    )
    s = livro('validar-briefing', 'teste', 'briefing-tema2.md')
    assert s.codigo == 0, f"código {s.codigo}; stderr: {s.erro}"
    assert s.texto == (
        'ok: 2 momentos, 4 passagens, 0 citações, 0 dados da web\n'
    )
