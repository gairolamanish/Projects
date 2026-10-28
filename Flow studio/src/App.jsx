
import { useCallback, useState } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  Panel,
  Handle,
  Position,
  useNodesState,
  useEdgesState,
  BackgroundVariant,
} from '@xyflow/react';

import '@xyflow/react/dist/style.css';
import './index.css';
import './App.css';

function ServiceNode({ data }) {
  return (
    <div className={`service-node ${data.tone || 'blue'}`}>
      <Handle type="target" position={Position.Left} />

      <div className="node-top">
        <span className="node-icon">{data.icon}</span>
        <span className="node-status">
          <i /> ONLINE
        </span>
      </div>

      <div className="node-title">{data.title}</div>
      <div className="node-subtitle">{data.subtitle}</div>

      <Handle type="source" position={Position.Right} />
    </div>
  );
}

const nodeTypes = {
  service: ServiceNode,
};

const serviceDetails = {
  gateway: {
    title: 'API Gateway',
    category: 'API MANAGEMENT',
    description:
      'Acts as an entry point for incoming API requests and routes them to the appropriate service.',
    uses: [
      'Route requests to different APIs',
      'Apply rate limits and request policies',
      'Centralize API access',
    ],
    example: 'Client → API Gateway → API Service',
  },

  rest: {
    title: 'REST API',
    category: 'API STYLE',
    description:
      'Uses HTTP methods and resource-based endpoints to exchange data, commonly in JSON format.',
    uses: [
      'Fetch or update user profiles',
      'Create posts and submit comments',
      'Build web and mobile application backends',
    ],
    example: 'GET /api/posts/101',
  },

  soap: {
    title: 'SOAP API',
    category: 'WEB SERVICES',
    description:
      'A messaging protocol that commonly uses XML envelopes for structured service communication.',
    uses: [
      'Enterprise integrations',
      'Banking and payment system integrations',
      'Legacy business applications',
    ],
    example: 'SOAP Request → XML Response',
  },

  graphql: {
    title: 'GraphQL API',
    category: 'API STYLE',
    description:
      'Lets clients request specific fields from a graph of related data through a defined schema.',
    uses: [
      'Instagram-like social feeds: posts, authors and engagement counts',
      'Profile screens: user details and related content',
      'E-commerce: product details, prices and reviews',
      'Dashboards that combine related information',
    ],
    example: `query GetFeed {
  user(id: "101") {
    username
    posts {
      caption
      likesCount
      commentsCount
    }
  }
}`,
    response: `{
  "data": {
    "user": {
      "username": "alex",
      "posts": [
        {
          "caption": "My weekend",
          "likesCount": 120,
          "commentsCount": 8
        }
      ]
    }
  }
}`,
    note:
      'Illustrative example only. Your GraphQL server must define these fields and resolvers for this query to work.',
  },

  auth: {
    title: 'Authentication',
    category: 'SECURITY',
    description:
      'Verifies a user or client identity before granting access to protected resources.',
    uses: [
      'User login and session management',
      'Token validation',
      'Access control for protected endpoints',
    ],
    example: 'Client → Verify Token → Allow or Deny',
  },

  backend: {
    title: 'Backend Services',
    category: 'APPLICATION LAYER',
    description:
      'Contains application logic and coordinates operations between APIs and data sources.',
    uses: [
      'Process business rules',
      'Validate incoming requests',
      'Coordinate database and external service calls',
    ],
    example: 'Request → Business Logic → Result',
  },

  analytics: {
    title: 'Data Services',
    category: 'DATA PROCESSING',
    description:
      'Provides data access, transformations, aggregation and processing for application features.',
    uses: [
      'Aggregate likes and comments',
      'Prepare dashboard statistics',
      'Fetch and transform application data',
    ],
    example: 'Data Sources → Processing → API Response',
  },

  database: {
    title: 'Database',
    category: 'DATA STORAGE',
    description:
      'Stores persistent application information and makes it available to authorized services.',
    uses: [
      'Store user profiles',
      'Save posts and comments',
      'Persist product, order and application records',
    ],
    example: 'Application Service ↔ Database',
  },
};

const initialNodes = [
  {
    id: 'gateway',
    type: 'service',
    position: { x: 30, y: 205 },
    data: {
      title: 'API Gateway',
      subtitle: 'Request routing',
      icon: '◈',
      tone: 'blue',
    },
  },
  {
    id: 'rest',
    type: 'service',
    position: { x: 330, y: 35 },
    data: {
      title: 'REST API',
      subtitle: 'HTTP / JSON',
      icon: '⇄',
      tone: 'blue',
    },
  },
  {
    id: 'soap',
    type: 'service',
    position: { x: 330, y: 205 },
    data: {
      title: 'SOAP API',
      subtitle: 'XML services',
      icon: '◇',
      tone: 'purple',
    },
  },
  {
    id: 'graphql',
    type: 'service',
    position: { x: 330, y: 375 },
    data: {
      title: 'GraphQL API',
      subtitle: 'Flexible queries',
      icon: '⬡',
      tone: 'pink',
    },
  },
  {
    id: 'auth',
    type: 'service',
    position: { x: 640, y: 35 },
    data: {
      title: 'Authentication',
      subtitle: 'Identity & access',
      icon: '⌑',
      tone: 'purple',
    },
  },
  {
    id: 'backend',
    type: 'service',
    position: { x: 640, y: 205 },
    data: {
      title: 'Backend Services',
      subtitle: 'Business logic',
      icon: '⚙',
      tone: 'green',
    },
  },
  {
    id: 'analytics',
    type: 'service',
    position: { x: 640, y: 375 },
    data: {
      title: 'Data Services',
      subtitle: 'Queries & processing',
      icon: '▥',
      tone: 'pink',
    },
  },
  {
    id: 'database',
    type: 'service',
    position: { x: 950, y: 205 },
    data: {
      title: 'Database',
      subtitle: 'Persistent storage',
      icon: '▤',
      tone: 'yellow',
    },
  },
];

const initialEdges = [
  { id: 'e1', source: 'gateway', target: 'rest', label: 'HTTP' },
  { id: 'e2', source: 'gateway', target: 'soap', label: 'XML' },
  { id: 'e3', source: 'gateway', target: 'graphql', label: 'Query' },
  { id: 'e4', source: 'rest', target: 'auth' },
  { id: 'e5', source: 'soap', target: 'backend' },
  { id: 'e6', source: 'graphql', target: 'analytics' },
  { id: 'e7', source: 'auth', target: 'backend' },
  { id: 'e8', source: 'backend', target: 'database' },
  { id: 'e9', source: 'analytics', target: 'database' },
].map((edge, index) => ({
  ...edge,
  type: 'smoothstep',
  animated: true,
  style: {
    stroke: ['#38bdf8', '#a78bfa', '#f472b6'][index % 3],
    strokeWidth: 2,
  },
  labelStyle: { fill: '#b8c9e4', fontSize: 10 },
  labelBgStyle: { fill: '#101c30' },
}));

export default function App() {
  const [nodes, , onNodesChange] = useNodesState(initialNodes);
  const [edges, , onEdgesChange] = useEdgesState(initialEdges);
  const [selectedId, setSelectedId] = useState(null);

  const selected = selectedId ? serviceDetails[selectedId] : null;

  const onNodeClick = useCallback((_, node) => {
  setSelectedId(node.id);
}, []);

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">✳</div>
          <div>
            <div className="eyebrow">DEVELOPER PLATFORM</div>
            <h1>Flow<span>Studio</span></h1>
          </div>
        </div>

        <div className="header-right">
          <span className="environment">ENVIRONMENT: DEV</span>
          <span className="live-badge"><i /> INTERACTIVE DEMO</span>
        </div>
      </header>

      <section className="intro">
        <div>
          <div className="eyebrow">ARCHITECTURE / API ECOSYSTEM</div>
          <h2>System <span>Architecture</span></h2>
          <p>
            Explore APIs, discover real-world use cases and inspect example
            requests.
          </p>
        </div>
        <div className="metric">
          <span>COMPONENTS</span>
          <strong>08</strong>
        </div>
        <div className="metric">
          <span>CONNECTIONS</span>
          <strong>09</strong>
        </div>
      </section>

      <section className="flow-frame">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          nodeTypes={nodeTypes}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={onNodeClick}
          fitView
          fitViewOptions={{ padding: 0.15 }}
          minZoom={0.2}
          maxZoom={1.8}
          proOptions={{ hideAttribution: true }}
        >
          <Background
            variant={BackgroundVariant.Dots}
            gap={22}
            size={1}
            color="#293b55"
          />
          <Controls />
          <MiniMap
            nodeColor={(node) =>
              ({
                blue: '#38bdf8',
                purple: '#a78bfa',
                pink: '#f472b6',
                green: '#34d399',
                yellow: '#fbbf24',
              })[node.data.tone] || '#64748b'
            }
            maskColor="rgba(5, 12, 24, 0.75)"
          />
          <Panel position="top-right">
            <div className="canvas-label">
              <span className="pulse-dot" /> CLICK ANY NODE TO EXPLORE
            </div>
          </Panel>
        </ReactFlow>
      </section>

      <footer className="footer">
        <div className="legend">
          <span><i className="blue-dot" /> API Layer</span>
          <span><i className="green-dot" /> Backend</span>
          <span><i className="yellow-dot" /> Data Layer</span>
        </div>
        <span className="footer-hint">
          Drag nodes · Scroll to zoom · Click a service
        </span>
      </footer>

      {selected && (
        <div
          className="details-backdrop"
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) {
              setSelectedId(null);
            }
          }}
        >
          <aside
            className="details-panel"
            role="dialog"
            aria-modal="true"
            aria-label={`${selected.title} details`}
          >
            <div className="details-header">
              <div>
                <div className="eyebrow">{selected.category}</div>
                <h2>{selected.title}</h2>
              </div>
              <button
                className="close-button"
                onClick={() => setSelectedId(null)}
                aria-label="Close details"
              >
                ✕
              </button>
            </div>

            <p className="details-description">{selected.description}</p>

            <h3>REAL-WORLD USE CASES</h3>
            <ul className="use-case-list">
              {selected.uses.map((use) => (
                <li key={use}>{use}</li>
              ))}
            </ul>

            <h3>EXAMPLE FLOW</h3>
            <div className="example-flow">{selected.example}</div>

            {selected.response && (
              <>
                <h3>EXAMPLE GRAPHQL QUERY</h3>
                <pre className="code-example">
                  <code>{selected.example}</code>
                </pre>

                <h3>SAMPLE JSON RESPONSE</h3>
                <pre className="code-example">
                  <code>{selected.response}</code>
                </pre>

                <p className="details-note">{selected.note}</p>
              </>
            )}

            <button
              className="done-button"
              onClick={() => setSelectedId(null)}
            >
              Back to architecture
            </button>
          </aside>
        </div>
      )}
    </main>
  );
}
