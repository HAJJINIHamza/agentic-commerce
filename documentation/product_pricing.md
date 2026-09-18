# Pricing modelization

LINK TO SOURCE : https://chatgpt.com/share/6a6ac384-5990-83ee-8fc2-24a6da2406ca

-------
There is still something I can't understand in our pricing optimization Let's take this example : product_cost = 3.65 shipping_cost = 4.57 plateform_fees = 1.74 advertising_cost = 1.39 payment_fees = 0.1 The total cost of this product (what I will pay for 1 unit of this product) is 11.45 so the minimum selling price is normally 11.45 $ However the way we compute the selling price is selling_price = fixed_cost / 1 - total_rate which will give you approximatively 20$ which increase the price a lot, which force us to set the price on shopee to minimum 21$, which is too much compared to the competition price, which is bad for us. I think there is something wrong here, what do you think and why not just consider our minimum price to 11.45 $ and set the price on shopee to something like 13-15 $ ?
-------

Yes — there is an important conceptual issue here, but it is slightly different from “the minimum selling price should be $11.45.”

The key is that you are mixing cost, break-even price, and target-profit price.

1. Your $11.45 is indeed your cost

You have:

Component	Cost
Product	$3.65
Shipping	$4.57
Platform fees	$1.74
Advertising	$1.39
Payment fees	$0.10
Total	$11.45

If these are genuinely per-order costs that do not depend on selling price, then:

Break-even price=$11.45
	​


At $11.45, you make $0 profit.

So your intuition here is correct.

2. But your fixed_cost / (1 - total_rate) formula is solving a different problem

That formula is appropriate when some of your costs are percentage-based.

For example, suppose Shopee + payment + advertising fees represent 20% of the selling price.

Then:

P=
1−0.20
11.45
	​

P=$14.31

Why?

Because at $14.31:

20%×14.31=$2.86

and therefore:

14.31−2.86=$11.45

You have exactly covered your $11.45 fixed costs.

So the formula itself isn't wrong.

The problem is how you're defining fixed_cost and total_rate.

3. I think this is the real issue in your current model

You gave:

platform_fees = $1.74
advertising_cost = $1.39
payment_fees = $0.10

If those numbers are already calculated dollar amounts for this product, you should not also put their percentage equivalents into total_rate.

That would effectively count them twice.

For example, imagine your current calculation is doing something like:

fixed_cost = 3.65 + 4.57 + 1.74 + 1.39 + 0.10
selling_price = fixed_cost / (1 - total_rate)

If total_rate already includes platform fee, payment fee, advertising fee, etc., then you're doing:

fixed dollar fees + percentage fees

for the same costs.

That can dramatically inflate the price.

4. There is another important problem: advertising cost

This is especially important for your Shopee model.

You currently have:

advertising_cost = $1.39

But advertising cost is not necessarily a fixed cost per unit.

It depends on things such as:

CPC
clicks
conversion rate
campaign performance

For example:

CPC = $0.15
Conversion rate = 5%

means:

20 clicks×$0.15=$3

per sale.

So advertising cost is better modeled as:

ad cost per sale=
conversion rate
CPC
	​


rather than blindly treating it as a permanent fixed cost.

5. So should you simply sell at $13–15?

Yes, potentially.

And this is where your pricing optimizer should become more intelligent.

You shouldn't necessarily say:

"My minimum price is $20, therefore I must sell at $21."

Instead, your system should distinguish between:

Break-even price

The lowest price at which:

Profit=0
Target-profit price

The price required to achieve your desired margin.

Market price

What competitors are actually charging.

These are three different things.

Let's use your example

Suppose your true non-percentage costs are:

3.65+4.57+1.39+0.10=9.71

And suppose the $1.74 platform fee is actually a percentage-based fee that happens to equal $1.74 at some reference selling price.

Then you should not treat $1.74 as both a fixed cost and a percentage fee.

Instead, model:

Profit(P)=P−C
product
	​

−C
shipping
	​

−C
ads
	​

−C
payment
	​

−P(r
platform
	​

)

or more generally:

Profit(P)=P(1−r
total
	​

)−C
fixed
	​

	​


That's the clean model.

6. And this leads to a much better pricing strategy for your AI system

Your optimizer should not start by calculating one "minimum selling price" and forcing Shopee to use it.

Instead:

Step 1 — Calculate true break-even price
P
BE
	​

=
1−r
C
fixed
	​

	​

Step 2 — Calculate target-profit price

For a target profit M:

P
target
	​

=
1−r
C
fixed
	​

+M
	​

Step 3 — Look at the market

Suppose:

Break-even = $12.10
Target-profit price = $15.20
Competitors = $12.99–$14.99

Your system should recognize:

"This product is economically possible, but achieving the desired margin may make it uncompetitive."

That's actually valuable information for your product-selection agent.

It might conclude:

❌ Don't sell this product.

rather than artificially pricing it at $20+ and hoping someone buys it.

7. Your $13–15 idea is therefore reasonable — with one condition

If:

P=$13

and your actual total costs after all applicable fees are $11.45, then:

Profit=13−11.45=$1.55

Margin:

13
1.55
	​

=11.9%

At $15:

Profit=15−11.45=$3.55

Margin:

15
3.55
	​

=23.7%

So $13–15 is not inherently wrong.

The question is whether $11.45 really represents your complete cost at that selling price.

That's the thing we need to verify.

The bigger correction I'd make to our architecture

Instead of:

minimum_selling_price
        ↓
pricing
        ↓
Shopee

I'd make it:

                 ┌── Break-even price
                 │
Product economics ├── Target-profit price
                 │
                 └── Maximum viable price
                          ↓
                    Market analysis
                          ↓
                 Competitive price range
                          ↓
                  Pricing optimizer
                          ↓
              Recommended Shopee price

And the optimizer should be allowed to say:

"This product cannot achieve the required margin while remaining competitive → reject product."

That is much more aligned with your product-scoring + pricing optimization objective.

So yes: I think you identified a real weakness in our previous pricing approach. The formula isn't mathematically wrong; we were using it in a way that can overinflate the price, especially if some costs were already expressed as dollar amounts and then represented again as rates.


------

Ok let's maintain our pricing model together : 

selling_price = fixed_cost * (1 - total_rate)
where I set : 
        fixed_cost = ( product_cost
                        + shipping_cost
                        + packaging_cost
                        + platform_fees
                        + advertising_cost
                        + payment_fees
                        )
and 
total_rate =         total_rate = (commission_rate 
                    + transaction_fee_rate 
                    + payoneer_fee_rate 
                    + service_fee_rate 
                    + ad_cost_rate 
                    + target_margin_rate )

this is largely heavy on our selling price, let's optimize 
In your oppinion what rates and what fixed cost should be deleted either because their equivalent in fixed cost exist, or their equivalent in total_rate exists, or simply because its not  relevant ? 

----


Yes. And first, there is a sign error in the formula you wrote.

It should be:

selling_price=
1−total_rate
fixed_cost
	​

	​


not:

fixed_cost(1−total_rate)

Now let's clean up the model carefully.

1. The biggest problem: double-counting

Your current model has:

Fixed costs

product cost
shipping cost
packaging cost
platform fees
advertising cost
payment fees

Rates

commission rate
transaction fee rate
Payoneer fee rate
service fee rate
ad cost rate
target margin rate

There are several overlaps here.

I would structure it like this
Cost / rate	Keep?	Where?	Reason
product_cost	✅	Fixed	Actual cost per unit
shipping_cost	✅	Fixed	Actual international shipping cost per unit
packaging_cost	⚠️	Fixed	Keep only if you actually pay it separately
platform_fees	❌	—	Delete if platform fees are already represented by commission/transaction/service rates
advertising_cost	❌	—	Delete if using ad_cost_rate
payment_fees	❌	—	Delete if payment fee is already represented by transaction/payment rate
commission_rate	✅	Rate	Shopee commission is percentage-based
transaction_fee_rate	✅	Rate	Percentage-based
payoneer_fee_rate	⚠️	Rate	Keep only if you actually pay Payoneer a percentage of the transaction
service_fee_rate	✅	Rate	If applicable to your Shopee setup
ad_cost_rate	⚠️	Rate	Better modeled separately from platform fees; don't double-count advertising
target_margin_rate	✅	Rate	This is your desired profit margin

So your simplified model becomes:

fixed_cost=product_cost+shipping_cost+packaging_cost
	​


and

total_rate=commission+transaction+service+payment+advertising+target margin
	​


But I would actually go one step further.

2. I would remove ad_cost_rate from this formula

Advertising is fundamentally different from commission and transaction fees.

For example:

CPC=$0.15

and

conversion rate=5%

gives:

ad cost/order=
0.05
0.15
	​

=$3

That's not naturally a percentage of selling price.

So I would calculate advertising outside the pricing formula.

For example:

advertising_cost_per_order=
conversion rate
CPC
	​


Then put that into fixed costs.

So:

fixed_cost=product+shipping+packaging+advertising_cost_per_order
	​


and:

total_rate=commission+transaction+service+payment+target margin
	​


This is much cleaner.

3. What about platform_fees?

This one is especially important.

If by:

platform_fees = $1.74

you mean that Shopee's commission, transaction fee, service fee, etc. together cost you $1.74 at a particular selling price, then do not put $1.74 in fixed costs.

Those fees should be calculated from their rates.

For example:

Selling price = $15
Commission = 8%
Transaction = 2%
Service = 3.5%

Then:

platform fees=15(0.08+0.02+0.035)
=$2.025

You don't need a separate $2.025 platform_fees variable in the pricing equation.

The rates already generate it.

4. Same problem with payment fees

If payment_fees = $0.10 is actually a percentage-based transaction/payment fee, then remove it from fixed costs.

If instead Shopee/Payoneer charges a true fixed $0.10 per transaction, then keep it in fixed costs.

This distinction is important:

Percentage fee
fee=P×r

→ rate

Fixed fee
fee=$0.10

→ fixed cost

5. So I'd propose this final model
Fixed costs
fixed_cost = (
    product_cost
    + shipping_cost
    + packaging_cost
    + advertising_cost_per_order
)
Variable rates
total_rate = (
    commission_rate
    + transaction_fee_rate
    + service_fee_rate
    + payment_fee_rate
    + target_margin_rate
)
Price
selling_price = fixed_cost / (1 - total_rate)

This is mathematically coherent.

6. But there's one more optimization I strongly recommend

I would not combine target_margin_rate with the actual cost rates into one variable conceptually.

Instead:

r
cost
	​

=r
commission
	​

+r
transaction
	​

+r
service
	​

+r
payment
	​


Then calculate:

P
break−even
	​

=
1−r
cost
	​

C
fixed
	​

	​

	​


And separately:

P
target
	​

=
1−r
cost
	​

−r
target
	​

C
fixed
	​

	​

	​


This gives your system two very useful numbers:

Break-even price: "Below this, we lose money."

Target price: "At this price, we achieve our desired margin."

That distinction will be extremely useful for your pricing optimizer.

7. And now your competitive-price problem becomes solvable

Suppose:

Fixed cost = $9.71
Commission = 8%
Transaction = 2%
Service = 3.5%
Payment = 2%
Target margin = 10%

Then:

r
cost
	​

=15.5%

Break-even:

P
BE
	​

=
1−0.155
9.71
	​

≈$11.49

Target:

P
target
	​

=
1−0.155−0.10
9.71
	​

≈$13.40

Now suppose competitors are selling at:

$12.99−$14.99

That's actually a good product.

Your optimizer could recommend roughly $13.40.

But if competitors were selling at:

$8.99−$10.99

then the system should say:

Reject product: target margin cannot be achieved at a competitive market price.

That's much better than forcing the product to $20.

So my recommended architecture is:
FIXED COSTS
├── product_cost
├── shipping_cost
├── packaging_cost
└── advertising_cost_per_order

VARIABLE RATES
├── commission_rate
├── transaction_fee_rate
├── service_fee_rate
└── payment_fee_rate

PROFIT TARGET
└── target_margin_rate

And remove from the current formula:

❌ platform_fees as a dollar amount
❌ advertising_cost as a dollar amount if you're using an ad-rate model
❌ payment_fees as a dollar amount if it's already represented by a percentage
❌ ad_cost_rate if we model advertising as CPC/conversion-rate-based cost

The one thing I'd want to verify before we lock this into your system is exactly how Shopee Singapore charges each of your fees (commission, transaction, service, payment, and advertising), because some may have fixed components or conditions. That could change which ones belong in the fixed-cost bucket versus the rate bucket.

-------------

ok now after estimating the minimum selling price using this : 
FIXED COSTS
├── product_cost
├── shipping_cost
├── packaging_cost
└── advertising_cost_per_order

VARIABLE RATES
├── commission_rate
├── transaction_fee_rate
├── service_fee_rate
└── payment_fee_rate

and considering our target margin to get the final selling price say 15$
now when you enter this number into shopee they add something else and the price become somehting like 20 $, I was wondering weather they are considering the same fees and rates that we already included in our formula, this will make cost redandant, do a deep search to verify this ? 
and tell me based on shopee pricing formula what are the fixed costs and rates that we should delete from our pricing model ?

-----------

Yes. I dug into this specifically, and I think we have identified the source of the confusion.

The important finding is:

Shopee's cross-border price calculation is not simply taking your $15 price and adding Shopee's commission/transaction/service fees on top of it.
The KRSC/Global SKU pricing mechanism uses a separate pricing formula involving Global SKU Price, Market Exchange Rate, Market Price Adjustment Rate, Service Fee Rate, and Cross-Border Shipping Cost, while the actual order settlement later deducts commissions, transaction fees, Payoneer fees, etc.

So if you enter what you consider a $15 "final selling price" and Shopee turns it into ~$20, we should not automatically assume Shopee is double-charging the same commission/transaction fees.

There is a much more important culprit.

1. What Shopee's pricing system actually does

Shopee's Korean Seller Center documentation describes the pricing mechanism with these components:

Global SKU Price
Market Exchange Rate
Market Price Adjustment Rate
Service Fee
Commission Fee
Transaction Fee
Cross-Border Shipping Cost / Hidden Fee

Shopee distinguishes between seller-controlled inputs and system-controlled inputs. The market exchange rate, market price adjustment rate and service fee are seller settings; commission, transaction fee and the actual cross-border shipping cost are system-controlled.

Most importantly, Shopee explicitly says that the Global SKU Price should already take into account things such as:

product purchase cost + domestic shipping + packaging + Payoneer withdrawal fee + desired margin

while the cross-border shipping cost is then handled automatically by the pricing logic.

That is very important for our architecture.

2. The $15 → $20 phenomenon is probably NOT Shopee adding 33% fees

Suppose:

Global SKU Price = $15

and Shopee produces something around:

Market price ≈ $20

That's a ratio of:

15
20
	​

=1.333

So we're talking about roughly a 33.3% uplift.

That's suspiciously close to what a Market Price Adjustment Rate could produce.

Shopee describes this setting as a mechanism for:

setting different prices between markets
adding additional margin
allowing room for seller promotions/discounts.

A third-party guide describing the same KRSC setting gives an example where a seller intentionally adds 30% to the Global SKU price to leave room for promotions and discounts.

So if your Market Price Adjustment Rate is around 30%, then:

15×(1+0.30)=19.50

And that's almost exactly your observed:

$15 → ~$20

This is a huge clue.

3. There is another thing Shopee adds: Cross-Border Shipping Cost

Shopee's KRSC documentation explicitly calls this a Hidden Fee and says it is automatically calculated according to the product's weight:

Cross Border Shipping Cost=international shipping cost−shipping subsidy/discount

This means we have to be extremely careful with our shipping_cost.

You previously told me that for your Korea → Singapore model, you were using something like:

Korea Post international shipping = ~$4.57

If that $4.57 is already the amount you will pay for international shipping, then we should NOT blindly add Shopee's automatically calculated Cross-Border Shipping Cost again.

However, we need to distinguish:

Your business shipping cost
supplier → Korean logistics/collection point → Singapore

from

Shopee's Cross-Border Shipping Cost

which is the shipping amount Shopee incorporates into the market listing price calculation.

Those aren't necessarily the same accounting item.

4. Now let's examine every variable in our model

Our current model was:

Fixed costs
product_cost
shipping_cost
packaging_cost
advertising_cost_per_order
Rates
commission_rate
transaction_fee_rate
service_fee_rate
payment_fee_rate
target_margin_rate

Now compare that against what Shopee's pricing mechanism actually does.

product_cost
KEEP

Shopee doesn't know your supplier's product cost.

So:

product_cost

must remain in our economic model.

packaging_cost
KEEP

Shopee's Global SKU pricing guidance explicitly says sellers should consider packaging costs when determining the Global SKU Price.

So this is our cost.

shipping_cost
KEEP — BUT VERIFY WHAT IT REPRESENTS

This is the most dangerous one.

If:

shipping_cost = actual Korea → Singapore cost

then it belongs in our profitability calculation.

But we must not also treat Shopee's Cross-Border Shipping Cost as another independent cost if it is merely the mechanism through which that shipping cost is recovered from the buyer/listing price.

We need to model the Shopee price conversion separately.

5. platform_fees
DELETE

This one should definitely not be in our fixed costs.

Shopee's commission and transaction fees are percentage-based deductions from the transaction/order amount. Shopee's documentation says commission is calculated as a rate applied to the product price after applicable seller discounts, while transaction fees are calculated as a percentage of the relevant order amount.

Therefore:

platform_fees = $X

should not be an independent fixed cost if commission_rate and transaction_fee_rate already represent those costs.

So:

DELETE platform_fees
	​

6. payment_fees

This needs to be split.

Transaction/payment processing fee

If by this you mean Shopee's transaction/PG fee:

DELETE payment_fees fixed amount
	​


and retain:

transaction_fee_rate

Shopee explicitly describes the transaction fee as a percentage-based fee.

Payoneer withdrawal fee

This is different.

Shopee's Korean documentation says Payoneer withdrawal fees can apply when withdrawing/transferring the settlement amount, with the cited example being 1.2% (or 0.9% through the Shopee Korea signup route).

So:

payoneer_fee_rate

can remain in our profitability model.

But it should not necessarily be part of Shopee's listing-price formula.

That's a distinction we were missing.

7. service_fee_rate
KEEP — but don't blindly assume a value

Shopee says the service fee is associated with programs/services such as Cashback/Free Shipping and can vary by country/service. If you aren't participating in an applicable program, it can be 0%.

And Shopee's Singapore Promo Xtra terms confirm that program service fees are charged in addition to transaction fees.

Therefore:

service_fee_rate

is a legitimate cost if your shop is actually enrolled in a program that charges it.

But it should not be automatically assumed to be 3.5%.

8. commission_rate
KEEP

Definitely.

Shopee explicitly charges a commission based on the applicable commission rate.

This is a real variable cost of selling.

However, here's the important part:

Don't add it twice.

If Shopee's Global SKU → Market price conversion is already designed to account for commission, then our system shouldn't treat the Shopee-generated price as our own pre-fee price and then add commission again.

Instead, we should calculate:

profit after Shopee fees

from the actual final customer price.

9. advertising_cost_per_order
KEEP in our profitability model

But do not put it into Shopee's Market Price Adjustment mechanism.

Shopee Ads are not a normal mandatory listing-price fee.

You decide:

CPC
conversion rate
advertising budget

and advertising cost happens when customers interact with your ads.

So:

AdCostPerOrder=
ConversionRate
CPC
	​


is appropriate for our economic model.

But Shopee's listing-price conversion should not be interpreted as automatically incorporating your future advertising spend.

10. The biggest correction: target_margin_rate

This is where I think our architecture needs to change.

Your target margin should NOT be something Shopee adds.

It is our optimization objective.

For example:

product + shipping + packaging + ads
        ↓
our cost
        ↓
Shopee fees
        ↓
target profit

We calculate the price necessary to achieve the target.

Shopee shouldn't be responsible for that.

11. So our model should now have TWO separate layers

This is the important architectural change.

Layer A — Our economic pricing model

We determine:

"What customer price do we need?"

Something like:

P
customer
	​

=
1−R
Shopee
	​

−R
Payoneer
	​

−R
target
	​

C
product
	​

+C
shipping
	​

+C
packaging
	​

+C
ads
	​

	​


where:

R
Shopee
	​

=R
commission
	​

+R
transaction
	​

+R
service
	​


with Payoneer handled separately depending on exactly how you define the margin.

12. Layer B — Shopee's price transformation

Then we ask:

"If I give Shopee a Global SKU Price of X, what price will Shopee display in Singapore?"

This is not the same equation.

Conceptually:

GlobalSKU→MarketExchangeRate→MarketPriceAdjustment→ServiceFee/otherShopeepricingparameters→CrossBorderShipping→CustomerPrice

The documentation confirms these are separate pricing inputs.

13. This explains your $15 → $20 observation

Imagine your desired economic price is:

P
target
	​

=$15

But your Shopee:

Market Price Adjustment Rate = 30%

Then Shopee may produce approximately:

15×1.30=$19.50

Now you see:

Our optimizer says $15
Shopee listing says ~$20

You might conclude:

"Shopee is adding another 33% of fees."

But it may actually be:

Shopee is applying the Market Price Adjustment Rate that YOU configured.

That is fundamentally different.

14. Therefore, what should we delete from our model?

Here is my current recommendation:

Variable	Our model	Reason
product_cost	✅ KEEP	Real supplier cost
shipping_cost	✅ KEEP	Real business cost
packaging_cost	✅ KEEP	Real business cost
platform_fees	❌ DELETE	Duplicate of Shopee percentage fees
advertising_cost_per_order	✅ KEEP	Real expected acquisition cost
payment_fees fixed amount	❌ DELETE	Duplicate if it represents transaction fee
commission_rate	✅ KEEP	Actual Shopee cost
transaction_fee_rate	✅ KEEP	Actual Shopee cost
service_fee_rate	✅ KEEP conditionally	Only if applicable
payoneer_fee_rate	✅ KEEP	Real settlement cost, but separate from Shopee listing formula
ad_cost_rate	❌ DELETE	Ads should be modeled via CPC/conversion or fixed expected cost
target_margin_rate	✅ KEEP	Our desired profit, not Shopee's fee
market_price_adjustment_rate	❌ DO NOT put in our cost model	Shopee price-setting mechanism
market_exchange_rate	❌ DO NOT put in cost model	Currency conversion
cross_border_shipping_cost	⚠️ Don't double-count	Shopee pricing mechanism vs our actual shipping expense
15. The model I would use going forward
Our internal economics

THIS IS THE FINAL MODEL: 

```

fixed_cost = (
    product_cost
    + shipping_cost
    + packaging_cost
    + advertising_cost_per_order
)

Then:

variable_rate = (
    commission_rate
    + transaction_fee_rate
    + service_fee_rate
    + payoneer_fee_rate
)

And:

required_customer_price = (
    fixed_cost
    / (1 - variable_rate - target_margin_rate)
)

```

BUT: we should not immediately call this the Shopee selling_price.

Let's call it:

required_customer_price

because that's what our economics require the customer to pay.

Then we need a second function:

shopee_market_price = shopee_price_transform(
    global_sku_price,
    market_exchange_rate,
    market_price_adjustment_rate,
    service_fee_rate,
    cross_border_shipping_cost
)

And this is where your $15 → $20 problem belongs.

16. One thing I don't want us to assume yet

I found authoritative documentation explaining the components of Shopee's formula, but the exact mathematical expression inside the current Seller Center UI is embedded in an image in Shopee's documentation rather than exposed as text in the page.

So I don't want to pretend we have verified the exact algebra of the current Singapore Seller Center from the documentation alone.

The best next step is actually very simple: give me a screenshot of the Shopee "Price Calculation Formula Setting" page from your Seller Center, especially the section showing:

Market Exchange Rate
Market Price Adjustment Rate
Service Fee Rate
any displayed formula/example

Then I can reconstruct the exact Shopee equation, plug your $15 → ~$20 example into it, and tell you exactly which of our variables are being duplicated and which ones are not.

That would let us lock down the pricing optimizer mathematically rather than guessing.