import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

import styles from './funnstyle.module.css';

export default function Home() {
	const {siteConfig} = useDocusaurusContext();
	return (
		/*<Layout
			title={`Circuit Docs`}
			description="Docs for the community, by the community.">
			<HomepageHeader />
			<main>
				<HomepageFeatures />
			</main>
		</Layout>*/
		<div className={styles.banner}>
			<img src='img/banner.jpg'></img>
			<div>
				<h1>Circuit Docs</h1>
				<h2>Homepage Coming Soon</h2>
			</div>
		</div>
	);
}
