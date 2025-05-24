from flask import Flask, render_template_string, jsonify, url_for
from datetime import datetime
import os

app = Flask(__name__)

# Configuração da data inicial
INICIO = datetime.strptime("2024-10-20 16:29:00", "%Y-%m-%d %H:%M:%S")

# Template HTML com CSS responsivo
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Relógio do Amor</title>
    <style>
        :root {
            --cor-primaria: #ff6b81;
            --cor-secundaria: #ff4757;
            --cor-fundo: #fff9f9;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: var(--cor-fundo);
            color: #333;
            line-height: 1.6;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            width: 100%;
            max-width: 500px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            padding: 25px;
            text-align: center;
            margin: 20px 0;
        }

        h1 {
            color: var(--cor-primaria);
            margin-bottom: 15px;
            font-size: clamp(1.5rem, 5vw, 2rem);
        }

        .couple {
            font-size: clamp(1.2rem, 4vw, 1.8rem);
            color: var(--cor-secundaria);
            font-weight: bold;
            margin: 15px 0;
        }

        .start-date {
            font-size: clamp(0.9rem, 3vw, 1.1rem);
            margin-bottom: 20px;
            color: #666;
        }

        .timer-container {
            background: #fff;
            border-radius: 10px;
            padding: 15px;
            margin: 20px 0;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
        }

        #timer {
            font-size: clamp(1rem, 4vw, 1.3rem);
            line-height: 1.8;
        }

        .heart {
            color: var(--cor-primaria);
            font-size: 1.5rem;
            display: inline-block;
            animation: pulse 1.5s infinite;
            margin: 0 5px;
        }

        /* Estilos do Carrossel */
        .carousel {
            position: relative;
            width: 300px;
            max-width: 500px;
            margin: 0 auto 20px;
            overflow: hidden;
            border-radius: 15px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
        }

        .carousel-inner {
            display: flex;
            transition: transform 0.5s ease;
        }

        .carousel-item {
            min-width: 100%;
            height: 400px;
            position: relative;
        }

        .carousel-item img {
            width: 300px;
            height: 100%;
            object-fit: cover;
        }

        .carousel-caption {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.5);
            color: white;
            padding: 10px;
            font-size: 0.9rem;
        }

        .carousel-control {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(255, 255, 255, 0.5);
            color: var(--cor-primaria);
            border: none;
            padding: 10px;
            cursor: pointer;
            z-index: 10;
            font-size: 1.5rem;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .carousel-control.prev {
            left: 10px;
        }

        .carousel-control.next {
            right: 10px;
        }

        .carousel-indicators {
            position: absolute;
            bottom: 0px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 5px;
            z-index: 10;
        }

        .indicator {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.5);
            cursor: pointer;
        }

        .indicator.active {
            background: var(--cor-primaria);
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.2); }
            100% { transform: scale(1); }
        }

        /* Ajustes para telas muito pequenas */
        @media (max-width: 400px) {
            .container {
                padding: 15px;
                border-radius: 10px;
            }

            #timer {
                font-size: 0.9rem;
            }

            .carousel-item {
                height: 200px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Carrossel de Imagens -->
        <div class="carousel">
            <div class="carousel-inner">
                <div class="carousel-item">
                    <img src="{{ url_for('static', filename='fotos/Carro.jpg') }}" alt="Foto do casal">
                    <div class="carousel-caption">Te amo meu love</div>
                </div>
                <div class="carousel-item">
                    <img src="{{ url_for('static', filename='fotos/Anonovo.jpg') }}" alt="Foto do casal">
                    <div class="carousel-caption">Nosso Ano Novo</div>
                </div>
                <div class="carousel-item">
                    <img src="{{ url_for('static', filename='fotos/pipa.jpg') }}" alt="Foto do casal">
                    <div class="carousel-caption">Nosso amor cresce a cada dia</div>
                </div>
            </div>
            <button class="carousel-control prev">❮</button>
            <button class="carousel-control next">❯</button>
            <div class="carousel-indicators">
                <div class="indicator active"></div>
                <div class="indicator"></div>
                <div class="indicator"></div>
            </div>
        </div>

        <h1>Relógio do Amor <span class="heart">❤️</span></h1>
        <p class="couple">Hemilli & Ailton</p>
        <p class="start-date">Juntos desde: 20/10/2024 16:29</p>

        <div class="timer-container">
            <p>Vocês estão juntos há:</p>
            <p id="timer">Carregando...</p>
        </div>
    </div>

    <script>
        // Script do Carrossel
        document.addEventListener('DOMContentLoaded', function() {
            const carouselInner = document.querySelector('.carousel-inner');
            const items = document.querySelectorAll('.carousel-item');
            const prevBtn = document.querySelector('.carousel-control.prev');
            const nextBtn = document.querySelector('.carousel-control.next');
            const indicators = document.querySelectorAll('.indicator');
            
            let currentIndex = 0;
            const totalItems = items.length;
            
            function updateCarousel() {
                carouselInner.style.transform = `translateX(-${currentIndex * 100}%)`;
                
                // Atualiza indicadores
                indicators.forEach((indicator, index) => {
                    indicator.classList.toggle('active', index === currentIndex);
                });
            }
            
            function nextSlide() {
                currentIndex = (currentIndex + 1) % totalItems;
                updateCarousel();
            }
            
            function prevSlide() {
                currentIndex = (currentIndex - 1 + totalItems) % totalItems;
                updateCarousel();
            }
            
            // Event listeners
            nextBtn.addEventListener('click', nextSlide);
            prevBtn.addEventListener('click', prevSlide);
            
            // Adiciona navegação pelos indicadores
            indicators.forEach((indicator, index) => {
                indicator.addEventListener('click', () => {
                    currentIndex = index;
                    updateCarousel();
                });
            });
            
            // Auto-avanço (opcional)
            let interval = setInterval(nextSlide, 5000);
            
            // Pausa o auto-avanço quando o mouse está sobre o carrossel
            const carousel = document.querySelector('.carousel');
            carousel.addEventListener('mouseenter', () => clearInterval(interval));
            carousel.addEventListener('mouseleave', () => {
                interval = setInterval(nextSlide, 5000);
            });
        });

        // Script do Relógio
        function updateTime() {
            fetch('/time')
                .then(response => {
                    if (!response.ok) throw new Error('Erro na rede');
                    return response.json();
                })
                .then(data => {
                    document.getElementById('timer').innerText = data.time;
                })
                .catch(error => {
                    console.error('Erro:', error);
                    document.getElementById('timer').innerText = "Atualizando...";
                    setTimeout(updateTime, 2000);
                });
        }

        // Atualiza imediatamente e a cada segundo
        updateTime();
        setInterval(updateTime, 1000);

        // Melhorias para mobile
        document.addEventListener('touchstart', function(){}, {passive: true});
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/time')
def time_elapsed():
    agora = datetime.now()
    diferenca = agora - INICIO

    dias = diferenca.days
    segundos_totais = diferenca.seconds
    horas = segundos_totais // 3600
    minutos = (segundos_totais % 3600) // 60
    segundos = segundos_totais % 60

    tempo_formatado = f"{dias} dias, {horas} horas, {minutos} minutos e {segundos} segundos"
    return jsonify({"time": tempo_formatado})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)