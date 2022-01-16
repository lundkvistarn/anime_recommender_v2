import React, { useState, useEffect } from "react";
import { Button, Container,Stack ,Row,Col,Form,Table } from 'react-bootstrap';
import PostForm from "./components/PostForm";
import "./App.css";

  class App extends React.Component {
    constructor(props) {
      super(props);
  
      this.state = {
        dataSynopsis: [],
        dataTitle: [],
        isLoadingSynopsis: false,
        isLoadingTitle: false,
        selectedValue: '',
      };
    }
  
    async getTitle() {
      try {
        const response = await fetch(
          '/title?title='+this.state.selectedValue,
        );
        const json = await response.json();
        const toJson = JSON.parse(json.name)
        console.log(toJson.data);
        this.setState({dataTitle: toJson.data});
      } catch (error) {
        console.log(error);
      } finally {
        this.setState({isLoadingTitle: false});
      }
    }

    async getSynopsis() {
      try {
        const response = await fetch(
          '/synopsis?title='+this.state.selectedValue,
        );
        const json = await response.json();
        const toJson = JSON.parse(json.name)
        console.log(toJson.data);
        this.setState({dataSynopsis: toJson.data});
      } catch (error) {
        console.log(error);
      } finally {
        this.setState({isLoadingSynopsis: false});
      }
    }
  
    componentDidMount() {
      //this.getRepos();
    }
  
    updateRepos(temp) {
      this.setState({selectedValue: temp, isLoading: true}, function () {
        this.getRepos();
      });
    }
    handleSubmitTitle = (event) => {
      event.preventDefault()
      console.log(event.target.elements.username.value);
      this.setState({selectedValue: event.target.elements.username.value, isLoadingTitle: true}, function () {
        this.getTitle();
      });
    }
    handleSubmitSynopsis = (event) => {
      event.preventDefault()
      console.log(event.target.elements.username.value);
      this.setState({selectedValue: event.target.elements.username.value, isLoadingSynopsis: true}, function () {
        this.getSynopsis();
      });
    }
    render() {
      const {selectedValue, isLoadingTitle,isLoadingSynopsis, dataTitle,dataSynopsis } = this.state;
  return (
    <Container className="main">
      <Row>
        <Col>
            <Form onSubmit={this.handleSubmitTitle}>
              <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Name of anime</Form.Label>
                <Form.Control  type="text"
                name="username" ref={node => (this.inputNode = node)} placeholder="Name of anime" />
              </Form.Group>
              <Button   disabled={isLoadingTitle} variant="primary" type="submit">Submit</Button>
            </Form>
            {isLoadingTitle ? (
          <p> waiting...</p>
        ) : <Table className="table" striped bordered hover size="sm">  <thead>
        <tr>
          <th>Name</th>
          <th>Members</th>
          <th>Score</th>
          <th>Similarity Score</th>
        </tr>
        </thead>
        <tbody> {(dataTitle.map(data =>  <tr>
      <td>{data.Name}</td>
      <td>{data.Members}</td>
      <td>{data.Score}</td>
      <td>{data.wr}</td>
    </tr>))}</tbody> </Table>}
        </Col>
      <Col>
      <Form onSubmit={this.handleSubmitSynopsis}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label>Description of anime</Form.Label>
              <Form.Control  type="text"
              name="username" ref={node => (this.inputNode = node)} placeholder="Description of anime" />
            </Form.Group>
            <Button   disabled={isLoadingSynopsis} variant="primary" type="submit">Submit</Button>
          </Form>
          {isLoadingSynopsis ? (
          <p> waiting...</p>
        ) : <Table className="table" striped bordered hover size="sm">  <thead>
        <tr>
          <th>Name</th>
          <th>Members</th>
          <th>Score</th>
          <th>Similarity Score</th>
        </tr>
        </thead>
        <tbody> {(dataSynopsis.map(data =>  <tr>
      <td>{data.Name}</td>
      <td>{data.Members}</td>
      <td>{data.Score}</td>
      <td>{data.wr}</td>
    </tr>))}</tbody> </Table>}
      </Col>
  </Row>
    </Container>
  );
}
}

export default App;
