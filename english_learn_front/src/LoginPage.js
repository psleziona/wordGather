import { Component } from "react";

class LoginPage extends Component {
    constructor() {
        super();
    }

    handleSubmit = e => {
        e.preventDefault();
        let form = new FormData()
        form.append('name', 'pablo')
        fetch('https://word-gather.herokuapp.com//login', {method: 'POST', body: form})
        .then(res => console.log(res))
    }

    render() {
        return (
            <form>
                <label htmlFor='name'>
                    <input name='name' />
                </label>
                <label htmlFor='submit'>
                    <input type='submit' name='submit' value='Login' onClick={this.handleSubmit}/>
                </label>
            </form>
        )
    }
}

export default LoginPage;