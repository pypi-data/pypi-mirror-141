import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import { requestAPI } from '../../handler';
import { Workflow } from './schema';
import { faFolderOpen } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';


// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IWorkflowsList {
  className?: string;
}

const WorkflowsList = ({ className }: IWorkflowsList): JSX.Element => {
  // ------------------------------------
  // Set up state
  // ------------------------------------
  const [workflows, setWorkflows] = useState<Workflow[]>([]);

  // ------------------------------------
  // Handle component initialisation
  // ------------------------------------
  const getWorkflows = async () => {
    const wfs = await requestAPI<any>('workflows');
    setWorkflows(Object.values(wfs))
  };

  useEffect(() => {
    getWorkflows();
  }, []);

  if (workflows.length === 0) {
    return (
      <div className={`workflows-list empty ${className}`}>
        <div className="empty">
          <h2>
            <FontAwesomeIcon icon={faFolderOpen} />
            No workflows installed.
          </h2>
        </div>
      </div>
    )
  }

  return (
    <div className={`workflows-list ${className}`}>
      <ul>
        {workflows.map((Item: Workflow) => (
          <li>
            <div className="workflow">
              <div>
                <div className="workflow-header">
                  <span>Version {Item.defaults.wfversion}</span>
                  <h3>{Item.name}</h3>
                </div>
                <div className="workflow-buttons">
                  <a className="workflow-url" href={Item.url}>
                    Github
                  </a>
                  <Link
                    className="workflow-link"
                    to={`/workflows/${Item.name}`}
                  >
                    <div>Open workflow</div>
                  </Link>
                </div>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledWorkflowsList = styled(WorkflowsList)`
  max-width: 1200px;
  margin: 50px auto 0 auto;

  > ul {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
    grid-template-rows: minmax(min-content, max-content);
    grid-column-gap: 20px;
    grid-row-gap: 20px;
    list-style: none;
  }

  .empty {
    width: 100%;
    height: 250px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
    background-color: #ffffff;
  }

  .empty svg {
    padding-right: 15px;
    color: lightgray;
  }

  .workflow {
    padding: 15px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
  }
  h3 {
    font-size: 24px;
  }

  .workflow span {
    color: #333;
  }

  .workflow-header span {
    letter-spacing: 0.05em;
    color: #a0a0a0;
    text-transform: uppercase;
    font-size: 11px;
    line-height: 1em;
    padding-bottom: 5px;
  }
  .workflow-header {
    display: flex;
    justify-content: space-between;
    flex-direction: column-reverse;
  }
  .workflow-buttons {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .workflow-link {
    color: #1d9655;
  }
  .workflow-buttons div {
    padding: 15px 25px;
    border: 1px solid #1d9655;
    color: #1d9655;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
  }
  .workflow-buttons div:hover {
    background-color: #1d9655;
    color: white;
  }
`;

export default StyledWorkflowsList;
