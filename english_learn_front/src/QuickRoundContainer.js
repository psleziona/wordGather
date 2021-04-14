import { Component } from 'react';
import QuickRound from './QuickRound';

class QuickRoundContainer extends Component {
    constructor() {
        super();
        this.state = {
            testStarted: false,
            total: 0,
            right: 0
        }
    }

    finishTest = () => {
        this.setState({
            testStarted: false
        })
    }

    gatherData = answers => {
        const total = answers.length;
        const right = answers.reduce((sum, elem) => {
            const isRight = Object.values(elem)[0]
            return isRight?sum + 1:sum
        }, 0)
        this.handleUpdateDb(answers);
        this.setState({
            total,
            right
        })
    }

    handleUpdateDb = stats => {
        fetch('/words', {
            method: 'POST',
            body: JSON.stringify(stats)
        })
        .then(res => console.log(res))
    }

    startTest = () => {
        this.setState({
            testStarted: true
        })
    }

    render() {
        if (this.state.testStarted) {
            return <QuickRound handleTest={this.finishTest} gatherData={this.gatherData}/>
        } else {
            return (
                <div>
                    <button onClick={this.startTest}>Start</button>
                    {this.state.total > 0 &&
                    <div>
                        <p>Total {this.state.total}</p>
                        <p>Right {this.state.right}</p>
                    </div>
                    }
                </div>
            )
        }
    }
}

export default QuickRoundContainer;