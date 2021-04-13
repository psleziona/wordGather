import { Component } from 'react';
import QuickRound from './QuickRound';

class QuickRoundContainer extends Component {
    constructor() {
        super();
        this.state = {
            testStarted: false
        }
    }

    finishTest = stats => {
        // this.handleUpdateDb(stats);
        const total = stats.answers.length;
        console.log(stats);
        this.setState({
            testStarted: false
        })
    }

    handleUpdateDb = stats => {
        fetch('/words', {
            method: 'POST',
            body: stats
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
            return <QuickRound handleTest={this.finishTest} />
        } else {
            return (
                <div>
                    <button onClick={this.startTest}>Start</button>
                </div>
            )
        }
    }
}

export default QuickRoundContainer;