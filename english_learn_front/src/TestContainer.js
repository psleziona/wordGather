import { Component } from "react";
import TestObject from "./TestObject";

class TestContainer extends Component {
    constructor(props) {
        super(props);
        this.state = {
            answers: []
        }
    }


    gatherData = (word, right) => {
        this.setState(prevState => {
            return {
                answers: [...prevState.answers, { [word]: right }]
            }
        })
    }


    shouldComponentUpdate(nextProps) {
        if (nextProps.tests == this.props.tests) {
            return false;
        }
        return true;
    }

    
    

    handleClick = () => {
        let notAnswered = [];
        this.props.tests.forEach(elem => {
            let word = elem.english_word;
            let x = this.state.answers.filter((obj) => {
                return word in obj;
            });
            if (x.length == 0) {
                notAnswered.push({ [word]: false })
            }
        });
        this.setState(prevState => {
            return {
                answers: [...prevState.answers, ...notAnswered]
            }
        }, this.updateStatus)
    }

    updateStatus = () => {
        fetch('https://word-gather.herokuapp.com/words', {
            method: 'POST',
            body: JSON.stringify(this.state.answers),
            credentials: 'include'
        })
            .then(res => {
                if (res.status == 200) {
                    this.props.handleSend();
                }
            })
    }


    render() {
        const tests = this.props.tests.map((elem, i) => {
            const { english_word, right_answers, false_answers } = elem;
            const rightAnswer = right_answers[Math.floor(Math.random() * right_answers.length)];
            let answers = [rightAnswer, ...false_answers];
            answers = answers.sort(() => Math.random() - .5);
            return (
                <TestObject key={i} word={english_word}
                    answers={answers} rightAnswer={rightAnswer} onAnswer={this.gatherData} />
            )
        })

        

        return (
            <div>
                {tests}
                <button onClick={this.handleClick}>Finish</button>
            </div>
        )
    }
}

export default TestContainer;