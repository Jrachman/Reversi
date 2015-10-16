// Edwin Ho | eaho1@uci.edu | 73901628 - KoizumiAI.hpp - ICS46 Project 2

#include "OthelloAI.hpp"

namespace eaho1{
	class KoizumiAI: public OthelloAI{
	public:
		//Returns the color of the current turn of the state
		OthelloCell turn(const OthelloGameState& state);

		//Given black or white, returns white or black respectively
		OthelloCell opposite(OthelloCell color);

		//Returns the score for a parameterized player
		int scoreForPlayer(const OthelloGameState& state, OthelloCell player);

		//Returns true if during the transition from one state to the next, a given player took over a given cell.
		bool cellCapturedBy(OthelloCell player, const OthelloGameState& previousState, const OthelloGameState& currentState, int x, int y);

		//Returns true if during the transition from one state to the next, a given player took over a corner cell.
		bool cornerCapture(OthelloCell player, const OthelloGameState& previousState, const OthelloGameState& currentState, int width, int height);

		//Returns true if during the transition from one state to the next, a given player took over a cell adjacent to a corner cell.
		bool adjacentCornerCapture(OthelloCell player, const OthelloGameState& previousState, const OthelloGameState& currentState, int width, int height);

		//Returns the number of pieces along the edge of the board that a given player possesses.
		int sumOfEdgePieces(OthelloCell player, const OthelloGameState& currentState, int width, int height);
		
		//Returns an integer calculation based on obtaining corners and edges, while peventing the opponent to do the same.
		int stateEval(const OthelloGameState& previousState, const OthelloGameState& currentState, OthelloCell initialTurn);

		//Recursive function that delves a number a steps ahead to return the evaluation at the leaf of a path.
		int search(const OthelloGameState& previousState, OthelloGameState& currentState, OthelloCell initialTurn, int depth);

		//Changes the currently saved best move and evaluation mapped to it if a better move is found through search.
		void updateBestMove(int& oldBestEval, int newBestEval, std::pair<int,int>& oldBestMove, std::pair<int,int> newBestMove);

		//Chooses an "intelligent" valid move on the board to move to.
		virtual std::pair<int, int> chooseMove(const OthelloGameState& state);		
	private:
		int defaultDepth = 2;	//The depth passed into search		
	};
}