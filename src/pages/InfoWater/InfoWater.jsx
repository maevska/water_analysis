import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './InfoWater.css';

const images = [
  '/img/water1.jpg',
  '/img/water2.jpg',
  '/img/water3.jpg',
  '/img/water4.jpg'
];

const InfoWater = () => {
  const [current, setCurrent] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrent((prev) => (prev + 1) % images.length);
    }, 3500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="info-page">
      <div className="info-content">
        <div className="info-text">
          <h1>Проблема загрязнения водоемов</h1>
          <p>
            Загрязнение водоемов — одна из самых острых экологических проблем современности. 
            Вода в реках, озерах и прудах подвергается воздействию промышленных, сельскохозяйственных и бытовых стоков, 
            что приводит к ухудшению качества воды, гибели водных организмов и угрозе здоровью человека.
          </p>
          <p>
            Основные источники загрязнения включают тяжелые металлы, нефтепродукты, удобрения, пестициды и бытовые отходы. 
            Последствия — цветение воды, снижение содержания кислорода, массовая гибель рыбы и ухудшение питьевой воды.
          </p>
          <p>
            Мониторинг и прогнозирование качества воды — важная задача для предотвращения экологических катастроф и сохранения водных ресурсов.
          </p>
          <button className="go-analysis-btn" onClick={() => navigate('/water-quality-analysis')}>
            Сделать прогноз
          </button>
        </div>
        <div className="info-slider">
          <img
            src={images[current]}
            alt="Водоем"
            className="slider-image"
            key={current}
          />
        </div>
      </div>
      <footer className="site-footer">
        <span>© 2025 Water Analysis</span>
        <span className="contacts">Контакты: water-analysis@mail.ru </span>
        </footer>
    </div>
  );
};

export default InfoWater;