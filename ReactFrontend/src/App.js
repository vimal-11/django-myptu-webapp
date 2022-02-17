import React, { useEffect, useState } from 'react';
import './App.css';
import Feeds from './components/feeds';
import FeedsLoadingComponent from './components/feedsLoading';

function App() {
	const FeedsLoading = FeedsLoadingComponent(Feeds);
	const [appState, setAppState] = useState({
		loading: false,
		posts: null,
	});

	useEffect(() => {
		setAppState({ loading: true });
		const apiUrl = `http://127.0.0.1:8000/feedsapi/`;
		fetch(apiUrl,{ 
			headers:{ 
				'Content-Type': 'application/json',
                'Accept': 'application/json'
			}
		})
			.then((data) => data.json())
			.then(data=>console.log(data))
			.then((posts) => {
				setAppState({ loading: false, posts: posts });
			});
	}, [setAppState]);
	return (
		<div className="App">
			<h1>Feeds</h1>
			<FeedsLoading isLoading={appState.loading} posts={appState.posts} />
		</div>
	);
}
export default App;