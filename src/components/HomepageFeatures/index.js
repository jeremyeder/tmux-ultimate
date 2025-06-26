import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: '🚀 Interactive Configuration',
    description: (
      <>
        No more manually researching hundreds of tmux options\! Answer a series of
        targeted questions and get a production-ready <code>.tmux.conf</code> file
        tailored to your workflow.
      </>
    ),
  },
  {
    title: '🎨 Beautiful Themes',
    description: (
      <>
        Choose from 5 carefully crafted color schemes: Dracula, Nord, Gruvbox, 
        Solarized, and Catppuccin. Visual previews help you pick the perfect theme
        for your terminal environment.
      </>
    ),
  },
  {
    title: '⚙️ Power User Focused',
    description: (
      <>
        Vim integration, TPM plugin management, system clipboard support, and 
        session logging. All the advanced features Linux power users need,
        configured with sensible defaults.
      </>
    ),
  },
];

function Feature({title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
EOF < /dev/null
