#!/usr/bin/env python3
"""
Macroeconomics (Gwartney 18e) practice quiz - Chapters 1, 2, 5, 6, 7, 8, 9, 10
Run:  python3 econ_quiz.py
No installs needed (standard library only).

Features
- Pick which chapters to practice
- Answer options are shuffled every time, so you learn the idea, not the letter
- Questions you miss come back at the end of the round until you get them right
- Missed questions are saved to ~/.econ_quiz_missed.json so you can do a
  "weak spots" round later
"""

import json
import os
import random
import textwrap

SAVE_FILE = os.path.expanduser("~/.econ_quiz_missed.json")

# In every question, the FIRST option is the correct one (they get shuffled on display).
QUESTIONS = [
    # ---------------- Chapter 1: The Economic Approach ----------------
    {"ch": 1, "q": "What is the opportunity cost of a choice?",
     "opts": ["The highest valued alternative that is sacrificed",
              "The total dollar price paid for the option",
              "The sum of all alternatives given up",
              "The cost of acquiring information about the option"],
     "exp": "Opportunity cost is the single highest-valued alternative you give up, not the sum of all alternatives. It's subjective and varies across people."},
    {"ch": 1, "q": "Which statement is NORMATIVE?",
     "opts": ["The inflation rate should be lower.",
              "The inflation rate rises when the money supply is increased.",
              "The earth is made of marshmallows.",
              "If gas prices rise, people will buy less gas."],
     "exp": "Normative = 'what ought to be' (should/ought), can't be proven true or false. Positive statements are testable even if false, like the marshmallow one."},
    {"ch": 1, "q": "Assuming that what is true for an individual must also be true for the whole group is called:",
     "opts": ["The fallacy of composition",
              "Violation of ceteris paribus",
              "Association is not causation",
              "The secondary effects pitfall"],
     "exp": "Fallacy of composition. Watch for it when moving from micro (individuals/firms) to macro (the whole economy)."},
    {"ch": 1, "q": "'Ceteris paribus' means:",
     "opts": ["Other things held constant",
              "At the margin",
              "Buyer beware",
              "Value is subjective"],
     "exp": "Ceteris paribus = other things constant. Failing to hold other things constant can lead to wrong conclusions about cause and effect."},
    {"ch": 1, "q": "When price is used to ration a good, who gets it?",
     "opts": ["Those willing and able to give up other things (pay the price)",
              "Those who arrive first",
              "Those with the most political influence",
              "Those who need it most"],
     "exp": "Price rationing allocates to those willing to give up other things, and it creates an incentive to earn income. First-come-first-served rewards waiting; government rationing rewards political status."},
    {"ch": 1, "q": "Economists say the test of a theory is:",
     "opts": ["Its ability to predict",
              "Whether experts agree with it",
              "Whether its assumptions are realistic",
              "Whether it is supported by good intentions"],
     "exp": "Principle 8: the test of a theory is its ability to predict real-world outcomes."},

    # ---------------- Chapter 2: Some Tools of the Economist ----------------
    {"ch": 2, "q": "A point INSIDE the production possibilities curve represents:",
     "opts": ["An inefficient use of resources",
              "An unattainable combination of output",
              "Full and efficient use of resources",
              "Economic growth"],
     "exp": "Inside = inefficient; you could get more of one good without giving up any of the other. On the curve = efficient. Outside = unattainable with current resources."},
    {"ch": 2, "q": "Which of these would NOT shift the PPC outward?",
     "opts": ["Moving resources from producing food to producing clothing",
              "An advancement in technology",
              "An increase in the economy's resource base",
              "Improvements in the rules under which the economy functions"],
     "exp": "Reallocating resources moves you ALONG the curve. The four outward shifters: more resources, better technology, improved rules/institutions, and working harder (giving up leisure)."},
    {"ch": 2, "q": "The law of comparative advantage says joint output is greatest when each good is produced by:",
     "opts": ["The low opportunity cost producer",
              "The producer who can make the most of it in absolute terms",
              "The producer with the most resources",
              "Whoever values the good most"],
     "exp": "Comparative advantage is about LOWER OPPORTUNITY COST, not absolute ability. It applies to individuals, firms, regions, and nations."},
    {"ch": 2, "q": "An economy that chooses more investment goods and fewer consumption goods today will likely:",
     "opts": ["See its PPC shift outward more in the future",
              "See its PPC shift inward in the future",
              "Move to a point inside its PPC",
              "Have no change in future production possibilities"],
     "exp": "Investing now (buildings, equipment, training) means greater future output, so the PPC shifts farther out compared with a high-consumption choice."},
    {"ch": 2, "q": "Middlemen (like your local grocer) are valuable mainly because they:",
     "opts": ["Reduce transaction costs",
              "Increase the price of goods",
              "Create property rights",
              "Eliminate opportunity costs"],
     "exp": "Middlemen reduce the time, effort, and resources needed to search out, negotiate, and complete an exchange (transaction costs)."},
    {"ch": 2, "q": "Which is NOT one of the three parts of private property rights?",
     "opts": ["The right to have the government set the property's price",
              "The right to exclusive use",
              "Legal protection against invaders",
              "The right to transfer it to another"],
     "exp": "Private property rights = exclusive use, legal protection against invasion, and the right to transfer (sell, rent, lease, etc.)."},
    {"ch": 2, "q": "When a voluntary exchange occurs:",
     "opts": ["Both parties expect to be made better off",
              "One party gains exactly what the other loses",
              "Value is only transferred, not created",
              "The good's objective value stays fixed"],
     "exp": "Mutual gain is the foundation of trade. Moving goods to people who value them more creates value."},

    # ---------------- Chapter 5: Difficult Cases for the Market ----------------
    {"ch": 5, "q": "The economically efficient level of an activity is where:",
     "opts": ["Marginal benefit equals marginal cost",
              "Marginal benefit is at its maximum",
              "Total cost is minimized",
              "Marginal cost is zero"],
     "exp": "Expand an activity as long as MB > MC; stop where MB = MC (Q2 on the graph). Below that you skip worthwhile units; beyond it MC > MB."},
    {"ch": 5, "q": "When external COSTS (negative externality) are present, the market will produce:",
     "opts": ["Too many units at too low a price",
              "Too few units at too high a price",
              "Too few units at too low a price",
              "The efficient quantity"],
     "exp": "The supply curve understates the true cost, so output is too high and price too low. Including all costs shifts supply left (S2): lower Q, higher P."},
    {"ch": 5, "q": "When external BENEFITS (positive externality) are present, the market will usually produce:",
     "opts": ["Too few units",
              "Too many units",
              "The efficient quantity",
              "Nothing at all"],
     "exp": "The demand curve understates the total value, so units worth more than they cost may not get produced. Counting all benefits shifts demand right."},
    {"ch": 5, "q": "The two defining characteristics of a public good are:",
     "opts": ["Nonrival in consumption and nonexcludable",
              "Produced by government and free of charge",
              "Rival in consumption and excludable",
              "Low cost and high demand"],
     "exp": "It's the good's characteristics, not who produces it. Examples: national defense, broadcast signals, mosquito abatement."},
    {"ch": 5, "q": "A person who receives the benefits of a good without helping pay for it is a:",
     "opts": ["Free rider",
              "Rent seeker",
              "Middleman",
              "Crony capitalist"],
     "exp": "Because nonpayers can't be excluded from public goods, people have an incentive to free ride, so too little of the good gets produced."},
    {"ch": 5, "q": "Which is NOT one of the four reasons the invisible hand (markets) may fail?",
     "opts": ["The special interest effect",
              "Lack of competition",
              "Externalities",
              "Poor information"],
     "exp": "Market failure: lack of competition, externalities, public goods, poor information. The special interest effect is a source of GOVERNMENT failure (Ch. 6)."},
    {"ch": 5, "q": "When competition is absent, sellers tend to:",
     "opts": ["Restrict output and raise prices",
              "Expand output and lower prices",
              "Produce the efficient quantity",
              "Create external benefits"],
     "exp": "Restricted supply (S2) gives Q2 < Q1 and P2 > P1: too few units at too high a price."},
    {"ch": 5, "q": "Protecting people and property and enforcing contracts is government's:",
     "opts": ["Protective function",
              "Productive function",
              "Redistributive function",
              "Regulatory function"],
     "exp": "Protective = security, rules, contract enforcement. Productive = providing goods hard to supply through markets (and a stable monetary environment)."},

    # ---------------- Chapter 6: The Economics of Political Action ----------------
    {"ch": 6, "q": "Voters having little incentive to become informed because their single vote is unlikely to be decisive is the:",
     "opts": ["Rational ignorance effect",
              "Shortsightedness effect",
              "Special interest effect",
              "Bundle purchase problem"],
     "exp": "Rational ignorance: getting informed is costly and one vote rarely changes the outcome, so many voters stay uninformed on many issues."},
    {"ch": 6, "q": "Representative government is biased toward adopting INEFFICIENT projects when:",
     "opts": ["Benefits are concentrated and costs are widespread",
              "Benefits and costs are both widespread",
              "Benefits are widespread and costs are concentrated",
              "Benefits and costs are both concentrated"],
     "exp": "Type 2: concentrated benefits + widespread costs = special interest effect. (Type 4, widespread benefits + concentrated costs, tends to REJECT productive projects.)"},
    {"ch": 6, "q": "Road project: benefits are Adams $20, Chan $12, Green $4, Lee $2, Diaz $2 (total $40). Under Plan A everyone pays $5 tax. What happens in a majority vote?",
     "opts": ["It fails 3 to 2, even though it's efficient",
              "It passes 3 to 2",
              "It passes unanimously",
              "It fails unanimously because it's inefficient"],
     "exp": "Only Adams and Chan gain more than $5. Green, Lee, Diaz vote no, so it fails 3-2 even though total benefits ($40) exceed costs ($25). Under Plan B (taxes proportional to benefits) it passes unanimously."},
    {"ch": 6, "q": "Politicians exchanging support on one issue for support on another is called:",
     "opts": ["Logrolling",
              "Pork-barrel legislation",
              "Rent seeking",
              "Crony capitalism"],
     "exp": "Logrolling = vote trading. Pork-barrel legislation = bundling many local spending projects into one bill."},
    {"ch": 6, "q": "Why do politicians find debt financing attractive, according to public choice analysis?",
     "opts": ["The shortsightedness effect: current benefits now, hard-to-see costs later",
              "The rational ignorance effect makes debt free",
              "Debt-financed projects are always efficient",
              "Bureaucrats prefer smaller budgets"],
     "exp": "Shortsightedness effect: bias toward clearly defined current benefits with future costs that are hard to identify."},
    {"ch": 6, "q": "Actions by groups trying to use the political process to redistribute income to themselves are called:",
     "opts": ["Rent (favor) seeking",
              "Entrepreneurship",
              "Logrolling",
              "Comparative advantage"],
     "exp": "Rent seeking diverts resources from productive activity, so output falls below potential."},
    {"ch": 6, "q": "The 'bootleggers and Baptists' strategy refers to:",
     "opts": ["Self-interested action packaged as moral behavior",
              "Voters trading votes across districts",
              "Bureaucrats seeking larger budgets",
              "Markets failing to provide public goods"],
     "exp": "Rent seekers frame favors as child safety, saving family farms, etc. Example: Mattel and the 2008 Consumer Product Safety Improvement Act."},
    {"ch": 6, "q": "The U.S. sugar program (concentrated gains for ~20,000 growers, ~$25 cost per household) illustrates:",
     "opts": ["The special interest effect",
              "The rational ignorance effect only",
              "A public good",
              "An efficient government program"],
     "exp": "Large personal benefit for a few + small individual cost spread over many = special interest effect. The program persists even though it's counterproductive."},
    {"ch": 6, "q": "Which is a source of GOVERNMENT failure?",
     "opts": ["Weak incentives for operational efficiency",
              "Externalities",
              "Public goods",
              "Lack of competition among sellers"],
     "exp": "Government failure: special interest effect, shortsightedness effect, rent seeking, weak incentives for operational efficiency (no profit motive, no bankruptcy)."},

    # ---------------- Chapter 7: Taking the Nation's Economic Pulse ----------------
    {"ch": 7, "q": "Why are intermediate goods NOT counted in GDP?",
     "opts": ["It would double count their value",
              "They are not produced domestically",
              "They are not sold for money",
              "They are counted in net exports instead"],
     "exp": "Only final goods and services count; the value of intermediate goods is already embodied in the final good."},
    {"ch": 7, "q": "Which is NOT a component of GDP under the EXPENDITURE approach?",
     "opts": ["Employee compensation",
              "Personal consumption",
              "Gross private investment",
              "Net exports"],
     "exp": "Expenditure approach: C + I + G + NX. Employee compensation is part of the resource cost-income approach (with self-employment income, rents, interest, profits)."},
    {"ch": 7, "q": "Nominal GDP is $27,361 billion and the GDP deflator is 122.3 (base year = 100). Real GDP in base-year dollars is about:",
     "opts": ["$22,372 billion", "$33,463 billion", "$27,361 billion", "$24,950 billion"],
     "exp": "Real GDP = Nominal GDP / (Deflator / 100) = 27,361 / 1.223 = about 22,372. (The 2023 figure in 2017 dollars from your slides.)"},
    {"ch": 7, "q": "How does the GDP deflator differ from the CPI?",
     "opts": ["The GDP deflator covers all goods in GDP; the CPI covers only what households buy",
              "The CPI is broader than the GDP deflator",
              "The GDP deflator only measures imported goods",
              "They use the exact same market basket"],
     "exp": "The GDP deflator is broader. It and the chained CPI also adjust for substitution away from goods that got relatively more expensive."},
    {"ch": 7, "q": "Which of these is NOT counted in GDP?",
     "opts": ["A homemaker cooking meals for their own family",
              "A family paying for a streaming subscription",
              "A firm buying new machinery",
              "The government building a highway"],
     "exp": "Household (nonmarket) production isn't counted because there's no market transaction. Other GDP shortcomings: underground economy, leisure, quality changes, 'bads'."},
    {"ch": 7, "q": "A hurricane destroys homes and infrastructure, then rebuilding begins. How is GDP affected?",
     "opts": ["Damages are not subtracted, but recovery spending is added",
              "Damages are subtracted and recovery spending is added",
              "Neither is counted",
              "Damages are subtracted and recovery spending is ignored"],
     "exp": "GDP tracks production, not destruction, so GDP can rise after a disaster. That's one reason GDP isn't a perfect welfare measure."},
    {"ch": 7, "q": "Between 2017 and 2023, nominal GDP rose 39.5%, but real GDP rose only 14.1%. Why?",
     "opts": ["Prices rose about 22% over the period",
              "Population fell",
              "Net exports were negative",
              "Intermediate goods were excluded"],
     "exp": "Nominal growth mixes higher output with higher prices. Deflating removes the price increase (deflator went 100 to 122.3)."},

    # ---------------- Chapter 8: Fluctuations, Unemployment, Inflation ----------------
    {"ch": 8, "q": "Population age 16+ = 250M, employed = 152M, unemployed = 8M. What is the UNEMPLOYMENT rate?",
     "opts": ["5.0%", "3.2%", "5.3%", "64%"],
     "exp": "Unemployment rate = unemployed / labor force. Labor force = 152 + 8 = 160M, so 8/160 = 5%. (Dividing by population is a common trap.)"},
    {"ch": 8, "q": "Same economy: population 16+ = 250M, employed = 152M, unemployed = 8M. What is the LABOR FORCE PARTICIPATION rate?",
     "opts": ["64%", "60.8%", "95%", "5%"],
     "exp": "LFPR = labor force / population 16+ = 160 / 250 = 64%. (152/250 = 60.8% is the employment-population ratio.)"},
    {"ch": 8, "q": "A person working part-time who is diligently searching for a full-time job is classified as:",
     "opts": ["Employed", "Unemployed", "Not in the labor force", "Cyclically unemployed"],
     "exp": "Working at least 1 hour for pay counts as employed, even if they want more hours."},
    {"ch": 8, "q": "A full-time college student who isn't working or looking for work is:",
     "opts": ["Not in the labor force", "Unemployed", "Employed", "Frictionally unemployed"],
     "exp": "Not working and not seeking work = not in the labor force (same for retirees and homemakers)."},
    {"ch": 8, "q": "An auto worker on temporary layoff who expects to be recalled is classified as:",
     "opts": ["Unemployed", "Employed", "Not in the labor force", "Discouraged worker"],
     "exp": "People on layoff waiting to return to a previous job count as unemployed."},
    {"ch": 8, "q": "Frictional unemployment is caused by:",
     "opts": ["Imperfect information as workers and employers search for good matches",
              "Workers' skills not matching available jobs",
              "A recession reducing demand for labor",
              "Not enough jobs for everyone"],
     "exp": "Frictional = job search under imperfect information. Structural = skill mismatch from changing products/technology. Cyclical = business cycle downturns."},
    {"ch": 8, "q": "New technology makes certain skills obsolete, and job openings require skills the unemployed don't have. This is:",
     "opts": ["Structural unemployment", "Frictional unemployment", "Cyclical unemployment", "Seasonal employment"],
     "exp": "Structural unemployment comes from structural changes in the economy that create a skills mismatch."},
    {"ch": 8, "q": "At full employment:",
     "opts": ["Only frictional and structural unemployment remain (no cyclical)",
              "The unemployment rate is zero",
              "Cyclical unemployment is at its peak",
              "Actual GDP is below potential GDP"],
     "exp": "Full employment = natural rate of unemployment, not zero. Actual output equals potential output."},
    {"ch": 8, "q": "During a recession, which is true?",
     "opts": ["Actual GDP is below potential GDP",
              "Actual unemployment is below the natural rate",
              "Employment exceeds full employment",
              "Cyclical unemployment is zero"],
     "exp": "In a recession, actual unemployment rises above the natural rate and actual GDP falls below potential."},
    {"ch": 8, "q": "The CPI was 150 at the end of last year and 157.5 at the end of this year. The inflation rate was:",
     "opts": ["5%", "7.5%", "4.8%", "57.5%"],
     "exp": "Inflation = (157.5 - 150) / 150 x 100 = 7.5 / 150 = 5%."},
    {"ch": 8, "q": "People expected 3% inflation, but prices rose 7%. This is:",
     "opts": ["Inflation higher than anticipated (unanticipated inflation)",
              "Anticipated inflation",
              "Inflation lower than anticipated",
              "Deflation"],
     "exp": "Actual exceeded expected, so 4 points of it was a surprise. Unanticipated inflation is what disrupts long-term contracts."},
    {"ch": 8, "q": "The four phases of the business cycle, in order starting from the top, are:",
     "opts": ["Peak, contraction, recessionary trough, expansion",
              "Expansion, peak, trough, contraction",
              "Peak, trough, contraction, expansion",
              "Contraction, peak, expansion, trough"],
     "exp": "Peak (boom) then contraction then recessionary trough (bottom) then expansion. A depression is a prolonged, very severe recession."},
    {"ch": 8, "q": "Which is NOT a reason high and variable inflation harms the economy?",
     "opts": ["It makes long-term contracts easier to plan",
              "It distorts the information delivered by prices",
              "It reduces investment by increasing risk",
              "People spend more time protecting wealth instead of producing"],
     "exp": "High, variable inflation makes long-term planning HARDER. It's hard to predict, which is exactly the problem."},

    # ---------------- Chapter 9: Basic Macroeconomic Markets ----------------
    {"ch": 9, "q": "Which is NOT a reason the aggregate demand curve slopes downward?",
     "opts": ["A higher price level improves firms' profit margins",
              "A lower price level increases the purchasing power of money",
              "A lower price level lowers interest rates, boosting spending",
              "A lower price level makes domestic goods cheaper relative to foreign goods"],
     "exp": "The profit-margin story explains why SRAS slopes UP. AD slopes down due to the wealth effect, the interest rate effect, and the international substitution effect."},
    {"ch": 9, "q": "Why is the long-run aggregate supply (LRAS) curve vertical?",
     "opts": ["A higher price level doesn't change resources, technology, or institutions",
              "Firms can't change output in the long run",
              "Prices are fixed by contracts in the long run",
              "Aggregate demand is constant in the long run"],
     "exp": "Full-employment output (YF) depends on resources, technology, and institutions, which the price level doesn't change. So output can't be sustainably expanded by higher prices."},
    {"ch": 9, "q": "Why does the SRAS curve slope upward?",
     "opts": ["Some costs are fixed by contracts, so an unexpected price rise boosts profits",
              "Higher prices increase the economy's resource base",
              "Consumers buy more when prices rise",
              "Interest rates fall when prices rise"],
     "exp": "In the short run, wages, interest rates, etc. are locked in by prior contracts, so an unanticipated higher price level widens profit margins and firms expand output."},
    {"ch": 9, "q": "The money interest rate is 11% and expected inflation is 5%. The real interest rate is:",
     "opts": ["6%", "16%", "11%", "2.2%"],
     "exp": "Real interest rate = money interest rate - inflationary premium = 11% - 5% = 6%."},
    {"ch": 9, "q": "If actual inflation turns out HIGHER than anticipated:",
     "opts": ["Borrowers gain at the expense of lenders",
              "Lenders gain at the expense of borrowers",
              "Neither gains, since the interest rate adjusts",
              "Both gain equally"],
     "exp": "Borrowers repay with dollars worth less than expected. If inflation is LOWER than anticipated, lenders gain. Correctly anticipated inflation favors neither."},
    {"ch": 9, "q": "When overall interest rates rise, prices of previously issued bonds:",
     "opts": ["Fall", "Rise", "Stay the same", "Become zero"],
     "exp": "Old bonds pay a fixed rate. When new bonds pay more, the old ones are less attractive, so their price falls. Inverse relationship."},
    {"ch": 9, "q": "With a market-determined exchange rate, a trade deficit is closely linked with:",
     "opts": ["A net inflow of capital", "A net outflow of capital", "A budget surplus", "A trade surplus"],
     "exp": "Imports - Exports = Capital inflow - Capital outflow. A trade deficit (imports > exports) is matched by net capital inflow."},
    {"ch": 9, "q": "When the economy is in long-run equilibrium:",
     "opts": ["Actual unemployment equals the natural rate AND the actual price level equals the anticipated one",
              "Unemployment is zero",
              "Actual GDP exceeds potential GDP",
              "Cyclical unemployment is high"],
     "exp": "Long-run equilibrium: AD, SRAS, and LRAS intersect; output = potential (YF); full employment; expectations about the price level turned out correct."},
    {"ch": 9, "q": "An unanticipated increase in the price level will, in the short run:",
     "opts": ["Expand output and employment",
              "Reduce output and employment",
              "Have no effect on output",
              "Permanently increase potential GDP"],
     "exp": "Real wages and other contracted costs lag, so profits rise and firms expand. In the long run, costs catch up and output returns to potential."},
    {"ch": 9, "q": "Using government taxation and spending to achieve macroeconomic goals is:",
     "opts": ["Fiscal policy", "Monetary policy", "Trade policy", "Rent seeking"],
     "exp": "Fiscal = taxes and spending. Monetary = control of the money supply and credit conditions."},
    {"ch": 9, "q": "Which market coordinates the actions of borrowers and lenders, with the interest rate as its price?",
     "opts": ["Loanable funds market", "Resource market", "Foreign exchange market", "Goods and services market"],
     "exp": "The four key markets: goods & services, resource, loanable funds, foreign exchange."},
    {"ch": 9, "q": "Are trade deficits necessarily bad?",
     "opts": ["It depends on whether the borrowed funds go to productive investment",
              "Yes, always",
              "No, never",
              "Only when the exchange rate is fixed"],
     "exp": "A trade deficit reflects capital inflow (borrowing from foreigners). Productive investment raises future income; funding consumption or unproductive uses lowers it."},

    # ---------------- Chapter 10: Dynamic Change & the AD-AS Model ----------------
    {"ch": 10, "q": "Which of these would shift aggregate demand to the RIGHT?",
     "opts": ["A stock market boom that increases real wealth",
              "An increase in the real interest rate",
              "Growing pessimism among consumers and businesses",
              "An increase in the exchange rate value of the nation's currency"],
     "exp": "AD shifts right with: more real wealth, lower real interest rates, optimism, higher expected inflation, higher incomes abroad, and a LOWER exchange rate value of the currency."},
    {"ch": 10, "q": "A decline in the exchange rate value of the dollar will tend to:",
     "opts": ["Increase AD, because U.S. goods become cheaper to foreigners",
              "Decrease AD, because imports become cheaper",
              "Shift LRAS to the right",
              "Have no effect on AD"],
     "exp": "A weaker dollar makes U.S. exports cheaper and imports pricier, so net exports and AD rise."},
    {"ch": 10, "q": "Which would shift BOTH LRAS and SRAS to the right?",
     "opts": ["An improvement in technology",
              "A temporary spell of favorable weather",
              "A temporary drop in resource prices",
              "A reduction in expected inflation"],
     "exp": "LRAS shifters (resources, technology/productivity, institutions) move SRAS in the same direction too. Weather, temporary resource price changes, and expected inflation shift only SRAS."},
    {"ch": 10, "q": "A drought that temporarily reduces crop output would:",
     "opts": ["Shift SRAS left but leave LRAS unchanged",
              "Shift both LRAS and SRAS left",
              "Shift AD left",
              "Shift LRAS left only"],
     "exp": "Temporary changes in productive capability shift SRAS only. The long-run capacity of the economy isn't altered."},
    {"ch": 10, "q": "Steady, predictable growth from capital formation and better technology will:",
     "opts": ["Shift LRAS right without disrupting macro equilibrium",
              "Cause a recession",
              "Cause an unsustainable boom",
              "Shift only SRAS"],
     "exp": "Anticipated changes let decision makers adjust ahead of time, so equilibrium isn't disrupted. Full-employment output rises from YF1 to YF2."},
    {"ch": 10, "q": "In the SHORT run, an unanticipated increase in AD causes:",
     "opts": ["A higher price level and output above long-run potential",
              "A lower price level and lower output",
              "A higher price level with no change in output",
              "Unemployment above the natural rate"],
     "exp": "Profit margins temporarily improve, output exceeds potential, and unemployment falls BELOW the natural rate (e.g., P105 and Y2 on the slide)."},
    {"ch": 10, "q": "In the LONG run, after an unanticipated increase in AD:",
     "opts": ["Resource prices rise, SRAS shifts left, and output returns to potential at a higher price level",
              "Output stays permanently above potential",
              "Resource prices fall and SRAS shifts right",
              "LRAS shifts right to match the new AD"],
     "exp": "Contracts get renegotiated, costs rise, SRAS shifts left, and you end at full-employment output with a higher price level (P110). The demand boost only expanded output temporarily."},
    {"ch": 10, "q": "After an unanticipated DECREASE in AD, what eventually returns the economy to long-run equilibrium?",
     "opts": ["Lower resource prices and lower real interest rates",
              "Higher resource prices and higher real interest rates",
              "A permanent leftward shift of LRAS",
              "Nothing; the economy stays in recession permanently"],
     "exp": "Weak demand lowers resource prices (SRAS shifts right) and real interest rates fall, stimulating AD. Output returns to potential at a lower price level (P90), but it can be a lengthy, painful process."},
    {"ch": 10, "q": "An unexpected event that temporarily increases or decreases aggregate supply is a:",
     "opts": ["Supply shock", "Demand shock", "Fiscal policy", "Shift in LRAS"],
     "exp": "Supply shocks catch people by surprise. Examples of negative ones: the 2022 Russia-Ukraine war's effect on wheat and energy, Hurricane Katrina."},
    {"ch": 10, "q": "A sharp, unexpected rise in the world price of oil will, in the short run:",
     "opts": ["Shift SRAS left, raising the price level and lowering output",
              "Shift SRAS right, lowering the price level and raising output",
              "Shift AD right, raising both price level and output",
              "Have no effect until LRAS shifts"],
     "exp": "Higher resource costs shift SRAS left: price level up (P110), output down (Y2). If the shock is permanent, LRAS shifts left too; if temporary, SRAS eventually moves back."},
    {"ch": 10, "q": "A temporary bumper crop from good weather would cause:",
     "opts": ["A lower price level and higher current GDP, with LRAS unchanged",
              "A higher price level and lower GDP",
              "A permanent rightward shift in LRAS",
              "A leftward shift in AD"],
     "exp": "Favorable, temporary supply shock: SRAS shifts right, price level falls (P95), output rises to Y2. Because it can't be counted on, LRAS stays put."},
    {"ch": 10, "q": "If the actual rate of inflation is LESS than anticipated, firms will tend to:",
     "opts": ["Incur losses and reduce output",
              "Earn higher profits and expand output",
              "Leave output unchanged",
              "Shift LRAS to the right"],
     "exp": "Lower-than-expected inflation acts like a fall in the price level relative to locked-in costs. Higher-than-expected inflation does the opposite and boosts output."},
    {"ch": 10, "q": "According to the AD-AS model, the two causes of recessions are:",
     "opts": ["Unanticipated reductions in AD and unfavorable supply shocks",
              "Anticipated increases in AD and favorable supply shocks",
              "Steady growth in LRAS and lower interest rates",
              "Higher wealth and consumer optimism"],
     "exp": "Recession = product prices low relative to costs. Booms come from unanticipated increases in AD and favorable supply shocks."},
    {"ch": 10, "q": "During a recession, real interest rates tend to:",
     "opts": ["Fall, which stimulates AD and helps the economy recover",
              "Rise, which deepens the recession",
              "Stay constant",
              "Rise, which stimulates investment"],
     "exp": "The two self-correcting forces: real resource prices and real interest rates. In a recession both fall; in a boom both rise and slow the economy."},
    {"ch": 10, "q": "What caused the 2008-2009 Great Recession in AD-AS terms?",
     "opts": ["Falling housing and stock prices reduced AD, and soaring oil prices reduced SRAS",
              "Rising housing prices increased AD",
              "A permanent improvement in technology shifted LRAS",
              "Falling oil prices increased SRAS"],
     "exp": "Housing prices fell after mid-2006 and stocks plunged in 2008 (less wealth, lower AD), energy prices surged in 2007-08 (lower SRAS), and confidence collapsed (AD fell further)."},
    {"ch": 10, "q": "Which would be MOST likely to throw the U.S. economy into a recession?",
     "opts": ["An unanticipated drop in AD from a sharp decline in consumer confidence",
              "Lower transaction costs from the growth of the Internet",
              "An unanticipated fall in the world price of oil",
              "Steady, anticipated growth in the capital stock"],
     "exp": "Unanticipated AD reductions cause recessions. Lower transaction costs and cheaper oil boost supply (cheaper oil hurts oil-producing states, though)."},
    {"ch": 10, "q": "Over the past several decades, how have U.S. expansions compared with recessions?",
     "opts": ["Expansions have been far lengthier than recessions",
              "Recessions have been longer than expansions",
              "They have been about equal in length",
              "There have been no recessions since 1950"],
     "exp": "E.g., the 2009-2020 expansion lasted 128 months, while most recessions lasted under a year and a half."},
]

CHAPTER_NAMES = {
    1: "The Economic Approach",
    2: "Some Tools of the Economist",
    5: "Difficult Cases for the Market & Role of Government",
    6: "The Economics of Political Action",
    7: "Taking the Nation's Economic Pulse (GDP)",
    8: "Fluctuations, Unemployment & Inflation",
    9: "Basic Macroeconomic Markets",
    10: "Dynamic Change & the AD-AS Model",
}

WIDTH = 78


def wrap(text, indent=""):
    return textwrap.fill(text, WIDTH, initial_indent=indent, subsequent_indent=indent)


def load_missed():
    try:
        with open(SAVE_FILE) as f:
            return set(json.load(f))
    except (OSError, ValueError):
        return set()


def save_missed(missed):
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(sorted(missed), f)
    except OSError:
        pass


def ask(idx, number, total):
    """Ask one question. Returns True if answered correctly, None if the user quit."""
    item = QUESTIONS[idx]
    correct = item["opts"][0]
    opts = item["opts"][:]
    random.shuffle(opts)
    letters = "abcd"[:len(opts)]

    print("\n" + "-" * WIDTH)
    print(f"[{number}/{total}]  Ch. {item['ch']}: {CHAPTER_NAMES[item['ch']]}")
    print(wrap(item["q"]))
    for letter, opt in zip(letters, opts):
        print(textwrap.fill(opt, WIDTH, initial_indent=f"   {letter}) ", subsequent_indent="      "))

    while True:
        ans = input("Your answer (or q to quit): ").strip().lower()
        if ans == "q":
            return None
        if ans in letters and ans:
            break
        print(f"  Type one of: {', '.join(letters)}")

    chosen = opts[letters.index(ans)]
    right_letter = letters[opts.index(correct)]
    if chosen == correct:
        print("  Correct!")
        print(wrap(item["exp"], "  "))
        return True
    print(f"  Not quite. Answer: {right_letter}) {correct}")
    print(wrap(item["exp"], "  "))
    return False


def run_round(pool):
    """Run through the pool; missed questions repeat at the end until correct."""
    saved_missed = load_missed()
    queue = pool[:]
    random.shuffle(queue)
    first_try_right = 0
    first_attempt = set()
    per_ch = {}
    number = 0

    while queue:
        idx = queue.pop(0)
        number += 1
        result = ask(idx, number, number + len(queue))
        if result is None:
            break
        ch = QUESTIONS[idx]["ch"]
        if idx not in first_attempt:
            first_attempt.add(idx)
            right, seen = per_ch.get(ch, (0, 0))
            per_ch[ch] = (right + (1 if result else 0), seen + 1)
            if result:
                first_try_right += 1
                saved_missed.discard(idx)  # nailed it first try: off the weak list
        if not result:
            saved_missed.add(idx)
            queue.append(idx)  # comes back later in the round

    save_missed(saved_missed)

    if first_attempt:
        n = len(first_attempt)
        print("\n" + "=" * WIDTH)
        print(f"First-try score: {first_try_right}/{n}  ({100 * first_try_right // n}%)")
        for ch in sorted(per_ch):
            right, seen = per_ch[ch]
            flag = "  <- review this" if right / seen < 0.75 else ""
            print(f"  Ch. {ch}: {right}/{seen}{flag}")
        print(f"Questions saved to weak spots: {len(saved_missed)}")
        print("=" * WIDTH)


def choose_chapters():
    chapters = sorted(CHAPTER_NAMES)
    print("\nChapters:")
    for ch in chapters:
        count = sum(1 for q in QUESTIONS if q["ch"] == ch)
        print(f"  {ch}: {CHAPTER_NAMES[ch]} ({count} questions)")
    raw = input("Enter chapter numbers separated by spaces (blank = all): ").strip()
    if not raw:
        return chapters
    picked = []
    for part in raw.replace(",", " ").split():
        if part.isdigit() and int(part) in CHAPTER_NAMES:
            picked.append(int(part))
    return picked or chapters


def main():
    print("=" * WIDTH)
    print("  MACROECONOMICS PRACTICE QUIZ  (Gwartney 18e, Ch. 1, 2, 5-10)")
    print("=" * WIDTH)
    while True:
        missed = load_missed()
        print("\nMenu:")
        print("  1) Practice all chapters")
        print("  2) Pick chapters")
        print(f"  3) Weak spots only ({len(missed)} saved)")
        print("  4) Clear weak spots")
        print("  5) Quit")
        choice = input("> ").strip()

        if choice == "1":
            run_round(list(range(len(QUESTIONS))))
        elif choice == "2":
            chs = choose_chapters()
            pool = [i for i, q in enumerate(QUESTIONS) if q["ch"] in chs]
            run_round(pool)
        elif choice == "3":
            pool = [i for i in missed if i < len(QUESTIONS)]
            if not pool:
                print("No weak spots saved yet. Nice!")
            else:
                run_round(pool)
        elif choice == "4":
            save_missed(set())
            print("Weak spots cleared.")
        elif choice == "5":
            print("Good luck Monday!")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGood luck Monday!")
