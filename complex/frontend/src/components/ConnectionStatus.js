import React from 'react';
import './styles/Login.css';
import './styles/custom.css';



const ConnectionStatus = ({width, error, data}) => {
    const renderCardItem = (label, id, value) => (
        <div className="card-title">
          <h6>
            {label}:
            <span id={id} className="badge bg-secondary text-light" style={{ float: 'right', marginTop: '-0.5px', marginLeft: '0.25rem' }}>
              {value}
            </span>
          </h6>
          <hr style={{ marginTop: '-4px', marginBottom: '-4px' }} />
        </div>
      );

    return (
        <div className="card mb-2 custom-card-light">
            <div className="card-title" style={{ paddingTop: '1rem', marginBottom: '0.5rem', textAlign: 'center' }}>
                <h4><b>Связь</b></h4>
            </div>
            <div className="card-body" style={{ paddingTop: '0rem', paddingBottom: '0.75rem' }}>
                {renderCardItem("Связь с контроллером СП", "SPConnection",   error ? '?' : 'да')}
                {renderCardItem("внутренние ошибки контроллера СП",    "InternalErrors", error ? '?' : '')}
            </div>
        </div>
    );
};

export default ConnectionStatus;