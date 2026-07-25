document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('formLogin');
    const botaoEntrar = document.getElementById('botao-entrar-login');
    const circulo = document.querySelector('.circulo-animado');
    const imagem = document.getElementById('imagemEvento');
    const som = document.getElementById('somEvento');
    const titulo = document.querySelector('.titulo-revelacao'); 

    if (!botaoEntrar || !form) {
        console.error("Botão ou formulário não foram encontrados no DOM!");
        return;
    }

    botaoEntrar.addEventListener('click', function(e) {
        e.preventDefault();

        // 1. Validação básica dos campos
        const cpfInput = form.querySelector('[name="cpf"]');
        const senhaInput = form.querySelector('[name="senha"]');

        if (cpfInput && !cpfInput.value) {
            alert("Por favor, preencha o CPF.");
            return;
        }
        if (senhaInput && !senhaInput.value) {
            alert("Por favor, preencha a Senha.");
            return;
        }

        // Bloqueia o botão para evitar múltiplos cliques
        botaoEntrar.disabled = true;

        // 2. DISPARA A ANIMAÇÃO DO CÍRCULO
        if (circulo) {
            circulo.style.display = 'block';
            circulo.style.opacity = '0.7';
            circulo.classList.remove('animar-circulo');
            void circulo.offsetWidth; // Força o navegador a reiniciar a animação CSS
            circulo.classList.add('animar-circulo');
        }

        // Aos 2.1 segundos: Imagem, Texto e Som
        setTimeout(() => {
            if (imagem) imagem.style.display = 'block';
            if (titulo) titulo.classList.add('mostrar-texto');
            
            if (som) {
                som.load();
                som.currentTime = 0.0;
                som.volume = 0.5;
                som.play().catch(err => console.log("Áudio bloqueado pelo navegador:", err));
                
                setTimeout(() => {
                    som.pause();
                    som.currentTime = 0;
                }, 500);
            }
            
            setTimeout(() => {
                if (imagem) imagem.style.display = 'none';
            }, 500);

        }, 2100);

        // 3. APÓS 3 SEGUNDOS DE ANIMAÇÃO: Pega o CSRF do formulário e envia para o Django
        setTimeout(() => {
            const formData = new FormData(form);
            const csrfInput = form.querySelector('[name=csrfmiddlewaretoken]');
            const csrfToken = csrfInput ? csrfInput.value : '';

            fetch(form.action || window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Erro na requisição: " + response.status);
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'sucesso') {
                    // Redireciona para a tela correta após o login
                    window.location.href = data.redirect_url;
                } else {
                    alert(data.mensagem || "CPF ou senha incorretos.");
                    botaoEntrar.disabled = false;
                }
            })
            .catch(error => {
                console.error('Erro na requisição Fetch:', error);
                // Fallback de segurança: se o fetch falhar por qualquer razão, envia o formulário normalmente
                form.submit();
            });

        }, 3000);
    });
});