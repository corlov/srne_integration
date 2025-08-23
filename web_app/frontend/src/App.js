import React from 'react';
import Login from './components/Login';
import ComplexStatus from './components/ComplexStatus';
import { useSelector } from 'react-redux';



import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import TabsPage from "./components/TabsPage";

const App = () => {
    const authData = useSelector((state) => state.auth);

    return (
        <div>
            <h1>РТК локальная консоль управления АК</h1>
            <div>
                    {authData.isAuthenticated ? (<ComplexStatus/>) : (<Login/>) }
            </div>
        </div>
    );


    // return (
    //     <div>
    //         <div>
    //             {authData.isAuthenticated ? (
    //                 <BrowserRouter>
    //                     <Routes>
    //                     <Route path="/*" element={<TabsPage />} />
    //                     {/* можно добавить другие маршруты приложения */}
    //                     </Routes>
    //                 </BrowserRouter>
    //             ) : (<Login/>) }
    //         </div>
    //     </div>
    // );

    // return (
    //     <BrowserRouter>
    //       <Routes>
    //         <Route path="/*" element={<TabsPage />} />
    //         {/* можно добавить другие маршруты приложения */}
    //       </Routes>
    //     </BrowserRouter>
    //   );
};

export default App;
