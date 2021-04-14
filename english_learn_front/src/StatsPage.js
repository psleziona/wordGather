import { Component } from "react";
import StatsContainer from './StatsContainer';

class StatsPage extends Component {
    constructor() {
        super();
        this.state = {
            stats: []
        }
    }

    getstats = () => {
        fetch('https://word-gather.herokuapp.com//words/stats')
        .then(res => res.json())
        .then(data => this.setState({
            stats: data
        }))
    }

    componentDidMount() {
        this.getstats();
    }

    render() {
        console.log(this.state)
        return (
            <div>
                {this.state.stats && 
                this.state.stats.map((elem, i) => {
                    return <StatsContainer key={i} word={elem.word} counter={elem.counter} progress={elem.progress} />
                })
                }
            </div>
        )
    }
}

export default StatsPage;