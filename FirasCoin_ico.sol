// Version of compiler 
pragma solidity >=0.4.22 <0.9.0;

contract firasCoin_ico {
    // The maximum number of Firas coins 
    uint public max_firascoin = 1000000;

    // Euro => Firas coin 
    uint public eur_to_firasCoin = 50;

    // The total number of FirasCoins that have been bought by the investors 
    uint public total_firasCoin_bought = 0;

    mapping(address => uint) equity_firasCoin;
    mapping(address => uint) equity_eur;

    // Checking if the investor can buy some FirasCoins
    modifier can_buy_firasCoin(uint eur_invested){
        require ( eur_invested * eur_to_firasCoin + total_firasCoin_bought <= max_firascoin );
        _;
    }

    // Getting the equity in FirasCoins of an investor 
    function equity_in_firasCoin(address investor) external constant returns (uint) {
        return equity_firasCoin[investor];
    }

    // Getting the equity in eur
    function equity_in_eur(address investor) external constant returns (uint) {
        return equity_eur[investor];
    }

    // Buying FirasCoins
    function buy_firasCoin(address investor , uint eur_invested) external 
    can_buy_firasCoin(eur_invested) {
        uint firasCoin_bought = eur_invested * eur_to_firasCoin;
        equity_firasCoin[investor] += firasCoin_bought;
        equity_eur[investor] = equity_firasCoin[investor] / eur_to_firasCoin;
        total_firasCoin_bought += firasCoin_bought;
    }

    // Selling FirasCoins
    function sell_firasCoin(address investor , uint firasCoin_to_sell) external {
        equity_firasCoin[investor] -= firasCoin_to_sell;
        equity_eur[investor] = equity_firasCoin[investor] / eur_to_firasCoin;
        total_firasCoin_bought -= firasCoin_to_sell;
    }
}