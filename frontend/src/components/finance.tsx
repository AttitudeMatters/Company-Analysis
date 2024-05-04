import React, {useState} from 'react';
import './finance.css'
import { Alert, Flex, Spin } from 'antd';


function Finance() {
    const [time, setTime] = useState('');
    const [companyName, setCompanyName] = useState('');
    const [year, setYear] = useState('');
    const [isVisible, setIsVisible] = useState(false);
    const [isLoadingVisible, setIsLoadingVisible] = useState(false);
    const handleCompanyNameChange = (event: { target: { value: React.SetStateAction<string>; }; }) => {
        setCompanyName(event.target.value);
    };

    const handleYearChange = (event: { target: { value: React.SetStateAction<string>; }; }) => {
        setYear(event.target.value);
    };
    const fetchTime = async () => {
        try {
            setIsLoadingVisible(true);
            setTimeout(()=>{
                setIsVisible(true);
                setIsLoadingVisible(false);
            }, 20000);
            return;

            const headers = new Headers();
            headers.append("Company-Name", companyName);
            headers.append("Year", year);
            const response = await fetch('http://127.0.0.1:5000', {
                headers: headers
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            setBusinessResult(data.business);
            setMarketResult(data.market);
            setCompetetionResult(data.competition);
            setManagementResult(data.management);
            setgMarginResult(data.gmargin);
            setoexpenseResult(data.oexpense);
            console.log(data)
            setTime(data.result);
        } catch (error) {
            setTime('Failed to fetch');
        }
    };

    // @ts-ignore
    return (
        <div className="App">
            <Spin tip="Loading" size="large" className="center-screen"
                  style={{ display: isLoadingVisible ? 'block' : 'none' }}>
                <div className="content" />
            </Spin>
            <header className="App-header">
                <div>
                    Company name:
                    <input
                        type="text"
                        placeholder="Company Name"
                        value={companyName}
                        onChange={handleCompanyNameChange}
                    />

                </div>
                <div>
                    Year:
                    <input
                        type="text"
                        placeholder="Year"
                        value={year}
                        onChange={handleYearChange}
                    />
                </div>
                <button onClick={fetchTime}>Get some insights!</button>
                <h1>Business</h1>
                {<p>{businessResult}</p>}

                <h1>Markets and Distribution</h1>
                {<p>{marketResult}</p>}

                <h1>Competition</h1>
                {<p>{competitionResult}</p>}
               
                <h1>Management’s Discussion and Analysis of Financial Condition and Results of Operations</h1>
                <p>{managementResult}</p>

                <h1>Gross Margin</h1>
                <p>{gmarginResult}</p>

                <h1>Operating Expenses</h1>
                <p>{oexpenseResult}</p>
               
            </header>

        </div>
    );
}

export default Finance;
