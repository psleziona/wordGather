import { Component } from "react";

class QuickRound extends Component {
    constructor() {
        super();
        this.state = {
            word: '',
            translates: []
        }
    }

    getWord = () => {
        fetch('/word')
        .then(res => res.json())
        .then(data => {
            const word = data.word;
            const translates = data.meaning;
            this.setState(state => {
                return {
                    word, translates
                }
            });
        });
        console.log(this.state)
    }

    handleInput = e => {
        if (e.key == 'Enter') {
            const answer = e.target.value;
            if (this.handleAnswer(answer)) {
                e.target.value = '';
                this.getWord()
            }
        }
    }

    handleAnswer = answer => {
        if (this.state.translates.includes(answer)) {
            return true;
        }
    }


    render() {
        return (
            <div>
                <button onClick={this.getWord}>Get</button>
                <p>{this.state.word}</p>
                <label htmlFor='answer'>
                    <input onKeyDown={this.handleInput} name='answer' />
                </label>
            </div>
        )
    }
}

export default QuickRound;