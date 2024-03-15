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
    <div className={clsx('hero hero--primary') + " CircuitBanner"}>
      <div className="IntroductionBanner">
          <div className="IntroductionBannerLogo">
            <img src="/img/logo_mainpage.svg" width={"371.1px"} height={"236.28px"} />
          </div>
          <div className="IntroductionBannerText">
            <h1 className="hero__title">{siteConfig.title}</h1>
            <p className="hero__subtitle">{siteConfig.tagline}</p>
            <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs">
            Docs
          </Link>
          <div style={{width: 2 + "px"}}></div>
          <Link
            className="button button--secondary button--lg"
            to="/guides">
            Guides
          </Link>
        </div>
          </div>
      </div>
    </div>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Circuit Docs`}
      description="Docs for the community, by the community.">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
