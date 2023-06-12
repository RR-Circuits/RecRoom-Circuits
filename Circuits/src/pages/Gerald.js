import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">🐔 Gerald the Chicken 🐔</h1>
        <p className="hero__subtitle">You found him! You found Gerald the chicken!<br />So... uh... Anyways here are the credits!</p>
        
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout>
      <HomepageHeader />
      <main>
      <div style={{height: 10 + "px"}}></div>
      <h2 style={{"text-align": "center"}}>Credits:</h2>
      <h3 style={{"text-align": "center"}}>Site, chip, script and more creator - Funn Punn</h3>
      <h3 style={{"text-align": "center"}}>Workflow maker - joksulainen</h3>
      <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="https://github.com/RR-Circuits/RecRoom-Circuits/graphs/contributors">
            Contributors
          </Link>
      </div>
      <div style={{height: 10 + "px"}}></div>
      </main>
    </Layout>
  );
}
