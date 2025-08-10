const Transfer_card_INF= ()=>{

    useEffect(() => {
        const fetchCardInfo = async () => {
            try {
                const cardInfos = await getPlayerCard(transaction.card_id);
                console.log(cardInfos);
            } catch (error) {
                console.error("خطا در دریافت اطلاعات کارت:", error);
            }
        };
        
        if (transaction?.card_id) {
            fetchCardInfo();
        }
    }, [transaction]);
    return
    
}