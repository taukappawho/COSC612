import React from 'react';
import Header from './Header';
import healthy from '../healthy.jpg';
import rice from '../rice.jpg';
import autumnsoup from '../autumnsoup.jpg';
import dessert from '../dessert.jpg';

function Home() {
  return (
    <div>
      <Header />
      <main>
        <h1>I Have No Mouth and I Must Eat</h1>
        <p>Here you can explore various recipes!</p>
        <section className="goodeats">
          <h6>**placeholder for view recipes**</h6>
          <div className="responsive">
            <div className="gallery">
              <a target="_blank" href={healthy} rel="noopener noreferrer">
                <img src={healthy} alt="Healthy Meals" />
              </a>
              <div className="desc">Healthy Meals</div>
            </div>
          </div>

          <div className="responsive">
            <div className="gallery">
              <a target="_blank" href={rice} rel="noopener noreferrer">
                <img src={rice} alt="Dinner Meals" />
              </a>
              <div className="desc">Dinner Meals</div>
            </div>
          </div>

          <div className="responsive">
            <div className="gallery">
              <a target="_blank" href={autumnsoup} rel="noopener noreferrer">
                <img src={autumnsoup} alt="Fall Meals" />
              </a>
              <div className="desc">Fall Meals</div>
            </div>
          </div>

          <div className="responsive">
            <div className="gallery">
              <a target="_blank" href={dessert} rel="noopener noreferrer">
                <img src={dessert} alt="Desserts" />
              </a>
              <div className="desc">Desserts</div>
            </div>
          </div>

          <div className="clearfix"></div>
        </section>
      </main>
    </div>
  );
}

export default Home;
