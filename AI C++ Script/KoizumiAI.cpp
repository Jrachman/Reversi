// Edwin Ho | eaho1@uci.edu | 73901628 - KoizumiAI.cpp - ICS46 Project 2

#include <ics46/factory/DynamicFactory.hpp>
#include "KoizumiAI.hpp"

ICS46_DYNAMIC_FACTORY_REGISTER(OthelloAI, eaho1::KoizumiAI, "Itsuki Koizumi (Required)");

namespace eaho1{
	int findMin(int n1, int n2){
		if (n1 < n2)
			return n1;
		else
			return n2;
	}

	int findMax(int n1, int n2){
		if (n1 > n2)
			return n1;
		else
			return n2;
	}
}

//Returns the color of the current turn of the state
OthelloCell eaho1::KoizumiAI::turn(const OthelloGameState& state){
	if (state.isBlackTurn())
		return OthelloCell::black;	
	return OthelloCell::white;
}

//Given black or white, returns white or black respectively
OthelloCell eaho1::KoizumiAI::opposite(OthelloCell color){
	switch(color){
		case OthelloCell::black:
			return OthelloCell::white;
		case OthelloCell::white:
			return OthelloCell::black;
		default:
			return OthelloCell::empty;
	}
}

//Returns the score for a parameterized player
int eaho1::KoizumiAI::scoreForPlayer(const OthelloGameState& state, OthelloCell player){
	switch(player){
		case OthelloCell::black:
			return state.blackScore();
		case OthelloCell::white:
			return state.whiteScore();
		default:
			return 0;
	}
}

//Returns true if during the transition from one state to the next, a given player took over a given cell.
bool eaho1::KoizumiAI::cellCapturedBy(OthelloCell player, const OthelloGameState& previousState, const OthelloGameState& currentState, 
										int x, int y){
	return (previousState.board().cellAt(x, y) != player && currentState.board().cellAt(x,y) == player);
}

//Returns true if during the transition from one state to the next, a given player took over a corner cell.
bool eaho1::KoizumiAI::cornerCapture(OthelloCell player, const OthelloGameState& previousState, const OthelloGameState& currentState,
	int width, int height){
	return (cellCapturedBy(player, previousState, currentState, 0, 0) ||
		cellCapturedBy(player, previousState, currentState, width, 0) ||
		cellCapturedBy(player, previousState, currentState, 0, height) ||
		cellCapturedBy(player, previousState, currentState, width, height));
}

//Returns true if during the transition from one state to the next, a given player took over a cell adjacent to a corner cell.
bool eaho1::KoizumiAI::adjacentCornerCapture(OthelloCell player, const OthelloGameState& previousState, const OthelloGameState& currentState,
	int width, int height){
	return (cellCapturedBy(player, previousState, currentState, 1, 0) ||
			cellCapturedBy(player, previousState, currentState, 0, 1) ||
			cellCapturedBy(player, previousState, currentState, 1, 1) ||
			cellCapturedBy(player, previousState, currentState, width-1, 0) ||
			cellCapturedBy(player, previousState, currentState, width-1, 1) ||
			cellCapturedBy(player, previousState, currentState, width, 1) ||
			cellCapturedBy(player, previousState, currentState, 0, height-1) ||
			cellCapturedBy(player, previousState, currentState, 1, height-1) ||
			cellCapturedBy(player, previousState, currentState, 1, height) ||
			cellCapturedBy(player, previousState, currentState, height-1, width-1) ||
			cellCapturedBy(player, previousState, currentState, height-1, width) ||
			cellCapturedBy(player, previousState, currentState, height, width-1));
}

//Returns the number of pieces along the edge of the board that a given player possesses.
int eaho1::KoizumiAI::sumOfEdgePieces(OthelloCell player, const OthelloGameState& currentState, int width, int height){
	int result = 0;
	for (int w = 2; w <= width-2; w++){		
		if (currentState.board().cellAt(w, 0) == player)
			result++;		
		else if (currentState.board().cellAt(w, height) == player)
			result++;
	}
	for (int h = 2; h <= height-2; h++){		
		if (currentState.board().cellAt(0, h) == player)
			result++;	
		else if (currentState.board().cellAt(width, h) == player)
			result++;
	}
	return result;
}

//Returns an integer calculation based on obtaining corners and edges, while preventing the opponent to do the same.
int eaho1::KoizumiAI::stateEval(const OthelloGameState& previousState, const OthelloGameState& currentState, OthelloCell initialTurn){
	int width = currentState.board().width()-1, height = currentState.board().height()-1;	

	//Check Corners ==> OWN capture ==> VERY HIGH evaluation
	if (cornerCapture(initialTurn, previousState, currentState, width, height))
		return 100;

	//Check Corners ==> OPPONENT capture ==> VERY LOW evaluation	
	else if(cornerCapture(opposite(initialTurn), previousState, currentState, width, height))
		return -100;

	//Check Adjacent to Corners ==> OWN capture ==> LOW evaluation
	else if(adjacentCornerCapture(initialTurn, previousState, currentState, width, height))
		return -50;

	//Check Adjacent to Corners ==> OPPONENT capture ==> HIGH evaluation
	else if(adjacentCornerCapture(opposite(initialTurn), previousState, currentState, width, height))
		return 50;

	//All other cases ==> the DIFFERENCE between the sum of my OWN edge pieces and my OPPONENTS edge pieces
	else{		
		return sumOfEdgePieces(initialTurn, currentState, width, height) - sumOfEdgePieces(opposite(initialTurn), currentState, width, height);
	}		
}

//Recursive function that delves a number a steps ahead to return the evaluation at the leaf of a path.
int eaho1::KoizumiAI::search(const OthelloGameState& previousState, OthelloGameState& currentState, OthelloCell initialTurn, int depth){
	if (depth <= 1){	//Count the already-made move from previous to currentState as the first traversal, thus ends at depth <= 1
		return stateEval(previousState, currentState, initialTurn);
	}
	else{
		if (initialTurn == turn(currentState)){	//If its my turn
			int bestForMe = -999;			
			for (int x = 0; x < currentState.board().width(); x++){	//For each valid move I can make from the currentState
				for (int y = 0; y < currentState.board().height(); y++){
					if (currentState.isValidMove(x, y)){
						std::unique_ptr<OthelloGameState> nextState = currentState.clone();
						nextState->makeMove(x, y);
						int eval = search(currentState, *nextState, initialTurn, depth - 1);
						bestForMe = findMax(bestForMe, eval);
					}
				}
			}
			return bestForMe;
		}
		else {		//If its my opponent's turn
			int worstForMe = 999;
			for (int x = 0; x < currentState.board().width(); x++){	//For each valid move that my opponent can make from s
				for (int y = 0; y < currentState.board().height(); y++){
					if (currentState.isValidMove(x, y)){
						std::unique_ptr<OthelloGameState> nextState = currentState.clone();
						nextState->makeMove(x, y);
						int eval = search(currentState, *nextState, initialTurn, depth - 1);
						worstForMe = findMin(worstForMe, eval);
					}
				}
			}
			return worstForMe;
		}
	}
}

//Changes the currently saved best move and evaluation mapped to it if a better move is found.
void eaho1::KoizumiAI::updateBestMove(int& oldBestEval, int newBestEval, std::pair<int,int>& oldBestMove, std::pair<int,int> newBestMove){
	if (newBestEval > oldBestEval){
		oldBestEval = newBestEval;
		oldBestMove	= newBestMove;
	}
}

//Chooses an "intelligent" valid move on the board to move to.
std::pair<int, int> eaho1::KoizumiAI::chooseMove(const OthelloGameState& state){
	OthelloCell initialTurn = turn(state);	//Finds and saves what color the AI is playing as and passes it along to the other functions
	std::pair<int, int> bestMove {0,0};
	int bestEval = -1000;	
	for (int x = 0; x < state.board().width(); x++){
		for (int y = 0; y < state.board().height(); y++){
			if (state.isValidMove(x, y)){				
				std::unique_ptr<OthelloGameState> currentState = state.clone();
				currentState->makeMove(x, y);

				//Check the evaluation of this first move before moving onto the evaluations of search - in case this move is better than those.
				updateBestMove(bestEval, stateEval(state, *currentState, initialTurn), bestMove, std::pair<int,int>{x,y});
				
				//Now compare the evaluation of later states to the current best move.
				int eval = search(state, *currentState, initialTurn, this->defaultDepth);
				updateBestMove(bestEval, eval, bestMove, std::pair<int,int>{x,y});			
			}
		}
	}	
	return bestMove;
}