<script>
    document.addEventListener("DOMContentLoaded", function() {
        const botao = document.getElementById('botaologin');
        const circulo = document.querySelector('.circulo-animado');
        const imagem = document.getElementById('imagemEvento');
        const som = document.getElementById('somEvento');
        const titulo = document.querySelector('.titulo-revelacao'); 

        // Garante o estado inicial (escondido)
        circulo.style.display = 'block';
        titulo.classList.remove('mostrar-texto');
        
        // Adiciona o evento de clique no botão
        botao.addEventListener('click', function() {
            // Desativa o botão temporariamente para evitar cliques duplos durante a animação
            botao.disabled = true;
            
            // Reinicia a animação do círculo
            circulo.style.opacity = '0.7'; // Restaura a opacidade caso tenha sumido antes
            circulo.classList.remove('animar-circulo');
            
            // Pequeno delay para resetar o CSS e disparar o movimento
            setTimeout(() => {
                circulo.classList.add('animar-circulo');
                
                // Exatamente 2.1 segundos depois (fim da ida / início da volta)
                setTimeout(() => {
                    // 1. Mostra a imagem
                    imagem.style.display = 'block';
                    
                    // 2. Faz o texto subir e aparecer
                    titulo.classList.add('mostrar-texto');
                    
                    // 3. Configura, define o volume e toca o áudio
                    som.load();
                    som.currentTime = 0.0;
                    som.volume = 0.5; // 50% de volume
                    som.play().catch(e => console.log("Áudio bloqueado:", e));
                    
                    // Para o áudio após 500ms
                    setTimeout(() => {
                        som.pause();
                        som.currentTime = 0;
                    }, 500);
                    
                    // 4. Esconde a imagem após meio segundo
                    setTimeout(() => {
                        imagem.style.display = 'none';
                    }, 500);

                }, 2100); // 2100ms = Fim da ida do círculo

            }, 50);
            
            // Reabilita o botão após a animação inteira terminar (3 segundos)
            setTimeout(() => {
                botao.disabled = false;
            }, 3000);
        });
    });
</script>