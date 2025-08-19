import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useSelector } from 'react-redux';
import { useDispatch } from 'react-redux';
import { logout } from './actions/Auth';
import ContorllerStatus from './ControllerStatus';
import ConnectionStatus from './ConnectionStatus';
import './styles/Login.css';
import './styles/custom.css';



const ComplexStatus = () => {
    const dispatch = useDispatch();
    const authData = useSelector((state) => state.auth);

    const [data, setData] = useState(null);
    const [error, setError] = useState('error');

    const fetchData = async () => {
        try {
        
          // http://192.168.1.193:8080/v1/dynamic_data?deviceId=2
          // http://localhost:5000/get_actual_data
          //const response = await axios.post('http://192.168.1.193:8080/v1/dynamic_data?deviceId=2', { });
          console.log('before GET')
          const response = await axios.get('http://localhost:5000/dynamic_data');
          console.log(response)
          if (response) {
            //alert('Logged in token = ' + response.data.token)
            console.log(response.data)
            setData(response.data)
            setError('')
          }

        } catch (err) {
          setError(err.message);
        }
      };

      useEffect(() => {
        fetchData();
        const intervalId = setInterval(fetchData, 2000);
        return () => {
          clearInterval(intervalId);
        };
      }, []);


    useEffect(() => {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css';
        document.head.appendChild(link);
    
        // Cleanup function to remove the link when the component unmounts
        return () => {
          document.head.removeChild(link);
        };
      }, []);
   
    // const renderCardItem = (label, id, value) => (
    //     <div className="card-title">
    //       <h6>
    //         {label}:
    //         <span id={id} className="badge bg-secondary text-light" style={{ float: 'right', marginTop: '-0.5px', marginLeft: '0.25rem' }}>
    //           {value}
    //         </span>
    //       </h6>
    //       <hr style={{ marginTop: '-4px', marginBottom: '-4px' }} />
    //     </div>
    //   );

    const logoutUser = async () => {
        dispatch(logout());
    };


    const [time, setTime] = useState('');
    useEffect(() => {
        const eventSource = new EventSource('http://localhost:5000/events');

        eventSource.onmessage = (event) => {
            setTime(event.data);
        };

        // Clean up the event source on component unmount
        return () => {
            eventSource.close();
        };
    }, []);

    return (
        <div className="container">
            <div>
                <div className="button-container">
                Пользователь: {authData.username}
                <button className="fixed-button" onClick={logoutUser}>Выход</button>
                </div>
            </div>

            {authData.username === 'admin' ? (
                <>
                  <ContorllerStatus width='50%' error={error} data={data}/>
                  <ConnectionStatus width='49%' error={error} data={data}/>
                </>
              ) : (
                <ContorllerStatus width='99%' error={error} data={data}/>
              )
            }

            <div>
                <p>Current Time: {time}</p>
            </div>
        </div>
  );
};

export default ComplexStatus;