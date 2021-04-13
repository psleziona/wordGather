import { Component } from "react";

class QuickRound extends Component {
    constructor() {
        super();
        this.state = {
            word: '',
            translates: [],
            rightCounter: 0,
            wordCounter: 0,
            wrongCounter: 0,
            showAnswerBtn: false,
            showAnswer: false,
            answers: []
        }
    }

    getWord = () => {
        if (this.showAnswer) {
            this.setState(prevState => {
                return {
                    answers: [...prevState.answers, { [this.state.word]: false }]
                }
            });
        }
        fetch('/word')
            .then(res => res.json())
            .then(data => {
                this.setState(prevState => {
                    return {
                        word: data.word,
                        translates: data.meaning,
                        wordCounter: prevState.wordCounter + 1,
                        wrongCounter: 0,
                        showAnswerBtn: false,
                        showAnswer: false
                    }
                })
            });
    }

    handleInput = e => {
        if (e.key == 'Enter') {
            const answer = e.target.value;
            if (this.handleAnswer(answer)) {
                e.target.value = '';
                this.getWord()
            } else {
                this.setState(prevState => {
                    return {
                        wrongCounter: prevState.wrongCounter + 1
                    }
                }, this.checkShowAnswer)
            }
        }
    }

    checkShowAnswer = () => {
        if (this.state.wrongCounter == 3) {
            this.setState({
                showAnswerBtn: true
            });
        }
    }

    handleAnswer = answer => {
        if (this.state.translates.includes(answer)) {
            if (!this.state.showAnswer) {
                this.setState(prevState => {
                    return {
                        rightCounter: prevState.rightCounter + 1,
                        answers: [...prevState.answers, { [this.state.word]: true }]
                    }
                });
            }
            return true;
        }
    }

    handleNext = () => {
        this.setState(prevState => {
            return {
                answers: [...prevState.answers, { [this.state.word]: false }]
            }
        });
        this.getWord();
    }

    componentDidMount() {
        this.getWord();
    }

    finishRound = () => {
        const stats = {
            answers: this.state.answers,
            right: this.state.rightCounter
        }
        // this.props.handleTest(this.state.answers, this.state.rightCounter);
        this.setState({
            answers: []
        })
        this.props.handleTest(stats);
    }

    componentWillUnmount() {
        this.finishRound();
    }   

    render() {
        return (
            <div>
                <button onClick={this.finishRound}>Finish</button>
                <button onClick={this.handleNext}>Next</button>
                <ul>
                    <li>{this.state.word}</li>
                    <li>Total words: {this.state.wordCounter}</li>
                    <li>Right answers: {this.state.rightCounter}</li>
                    {this.state.wrongCounter > 0 ? <li>Wrong on current word: {this.state.wrongCounter}</li> : null}
                </ul>
                <label htmlFor='answer'>
                    <input onKeyDown={this.handleInput} name='answer' />
                </label>
                {this.state.showAnswerBtn ?
                    <button onClick={() => { this.setState({ showAnswer: true }) }}>Pokaz znaczenia</button> : null}
                {this.state.showAnswer &&
                    <ul>
                        {this.state.translates.map((elem, i) => {
                            return <li key={i}>{elem}</li>
                        })}
                    </ul>
                }
            </div>
        )
    }
}

export default QuickRound;