#!/usr/bin/env python3
"""
Macroeconomics (Gwartney 18e) practice quiz - Chapters 1, 2, 5, 6, 7, 8, 9, 10 (200 questions, 25 per chapter)
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
    # Generated from the web quiz's question data (econ_quiz.html), in the same order, so a
    # question's position here matches its id there. The FIRST option is always the correct one.
    # Retired questions are kept (never asked) so saved weak-spot numbers keep pointing to the
    # same questions.
    # id 0
    {'ch': 1,
     'q': 'Which best describes the opportunity cost of a choice?',
     'opts': ['The single highest-valued option given up by making the choice',
              'The combined value of every alternative that was passed over',
              'The money price paid to obtain the option that was selected',
              'The value of the chosen option minus what it cost to obtain'],
     'exp': 'Opportunity cost is the value of the single best alternative you give up. Because you '
            'could have taken only one alternative instead, that highest-valued option is the true '
            'cost of the choice.',
     'why': [None,
             'Adding up every alternative overstates the cost: you could have chosen only one of them '
             'instead, so only the highest-valued one is actually sacrificed.',
             'The money price is only part of the picture. Opportunity cost is the value of the best '
             'forgone alternative, which includes things like time, not just dollars paid.',
             'Value minus cost describes the net gain from the choice, not its cost. Opportunity cost '
             'looks at what was given up, not at what the choice yielded.']},
    # id 1
    {'ch': 1,
     'q': 'Which of these statements is normative?',
     'opts': ['Congress ought to bring the inflation rate down',
              'Raising the money supply tends to push inflation up',
              'The core of the earth is made mostly of marshmallow',
              'Higher gasoline prices lead drivers to buy less gas'],
     'exp': 'Normative statements are judgments about what ought to be; they reflect subjective values '
            "and can't be proved true or false. Saying Congress ought to lower inflation is exactly "
            'that kind of value judgment.',
     'why': [None,
             'This is a cause-and-effect claim about what is, which could be checked against data, so '
             'it is a positive statement.',
             "Being obviously false doesn't make a statement normative. It is a testable claim about "
             'what is, so it is positive; positive statements need not be correct.',
             'This describes how drivers actually respond to prices, a claim that evidence can test, '
             'so it is a positive statement.']},
    # id 2
    {'ch': 1,
     'q': 'The mistaken belief that what is true for one part must also be true for the whole group is '
          'called:',
     'opts': ['The fallacy of composition',
              'Association is not causation',
              'Violation of ceteris paribus',
              'Ignoring secondary effects'],
     'exp': 'The fallacy of composition is the mistaken belief that what is true for an individual or '
            'a part must also be true for the whole group. Economists watch for it when moving from '
            'micro units to the whole economy.',
     'why': [None,
             'Association versus causation is about wrongly concluding that one thing causes another '
             'because they move together, not about reasoning from a part to the whole.',
             'A ceteris paribus violation means failing to hold other factors constant when describing '
             'a change, not generalizing from one member to the group.',
             'Secondary effects are indirect, hard-to-see consequences of an action or policy. That is '
             'a different pitfall from assuming the whole behaves like its parts.']},
    # id 3 (retired)
    {'ch': 1,
     'q': "'Ceteris paribus' means:",
     'opts': ['Other things held constant', 'At the margin', 'Buyer beware', 'Value is subjective'],
     'exp': 'Ceteris paribus = other things constant. Failing to hold other things constant can lead '
            'to wrong conclusions about cause and effect.',
     'retired': True},
    # id 4
    {'ch': 1,
     'q': 'When price is used to ration a good, who ends up with it?',
     'opts': ['Those willing to give up the most other things to obtain it',
              'Those who arrive first and are willing to wait in line for it',
              'Those who have the strongest political connections to get it',
              'Those whose need for the good is judged to be the greatest'],
     'exp': 'When price rations a good, it goes to those willing to give up other things, by paying '
            'the price, to obtain ownership. That is also why price rationing gives people an '
            'incentive to earn income.',
     'why': [None,
             'Waiting in line describes first-come, first-served rationing, a different method. Under '
             "price rationing, arriving early doesn't help if you won't pay the price.",
             'Political connections describe allocation by influence, not by price. In a market, the '
             'good goes to whoever is willing to give up the most other things to buy it.',
             "Price doesn't measure anyone's judged need; it allocates to those willing to give up "
             'other things for the good. Allocating by need would require some other rationing '
             'method.']},
    # id 5
    {'ch': 1,
     'q': 'According to Gwartney, how should an economic theory be judged?',
     'opts': ['By how well it predicts real-world outcomes',
              'By how realistic each of its assumptions is',
              'By how many leading experts agree with it',
              'By whether its policy goals are well-meant'],
     'exp': 'Guidepost 8 says the test of a theory is its ability to predict. Economic thinking is '
            'scientific thinking: a theory is built from basic principles and then checked against '
            'real-world events.',
     'why': [None,
             'Theories rely on simplifying assumptions. A theory with unrealistic assumptions is still '
             "useful if its predictions hold up, so realism of assumptions isn't the test.",
             "Expert agreement isn't the scientific test. A theory is judged by testing its "
             'predictions against real-world events, not by a count of supporters.',
             "Good intentions don't make a theory correct. Judging by goals mixes in normative values; "
             'a theory is tested by whether its predictions come true.']},
    # id 6 (retired)
    {'ch': 2,
     'q': 'A point INSIDE the production possibilities curve represents:',
     'opts': ['An inefficient use of resources',
              'An unattainable combination of output',
              'Full and efficient use of resources',
              'Economic growth'],
     'exp': 'Inside = inefficient; you could get more of one good without giving up any of the other. '
            'On the curve = efficient. Outside = unattainable with current resources.',
     'retired': True},
    # id 7 (retired)
    {'ch': 2,
     'q': 'Which of these would NOT shift the PPC outward?',
     'opts': ['Moving resources from producing food to producing clothing',
              'An advancement in technology',
              "An increase in the economy's resource base",
              'Improvements in the rules under which the economy functions'],
     'exp': 'Reallocating resources moves you ALONG the curve. The four outward shifters: more '
            'resources, better technology, improved rules/institutions, and working harder (giving up '
            'leisure).',
     'retired': True},
    # id 8
    {'ch': 2,
     'q': 'The law of comparative advantage says the joint output of trading partners is greatest when '
          'each good is produced by:',
     'opts': ['The partner with the lower opportunity cost of producing it',
              'The partner who can make more of it with the same resources',
              'The partner whose workers earn the lower money wage per hour',
              'The partner who places the higher value on consuming the good'],
     'exp': 'The law of comparative advantage says joint output is greatest when each good is produced '
            'by the low opportunity cost producer. Each partner should specialize where it gives up '
            'the least of other goods.',
     'why': [None,
             'Making more with the same resources is absolute advantage. A partner can be better at '
             'everything and still be the high opportunity cost producer of one good.',
             "Money wages aren't the test. Comparative advantage depends on how much of other goods "
             'each partner gives up to make one more unit.',
             "How much someone values consuming a good doesn't decide who should produce it. "
             'Production should go to whoever has the lower opportunity cost.']},
    # id 9 (retired)
    {'ch': 2,
     'q': 'An economy that chooses more investment goods and fewer consumption goods today will '
          'likely:',
     'opts': ['See its PPC shift outward more in the future',
              'See its PPC shift inward in the future',
              'Move to a point inside its PPC',
              'Have no change in future production possibilities'],
     'exp': 'Investing now (buildings, equipment, training) means greater future output, so the PPC '
            'shifts farther out compared with a high-consumption choice.',
     'retired': True},
    # id 10
    {'ch': 2,
     'q': 'Why are people willing to pay middlemen such as grocers, real estate agents, and online '
          'marketplaces?',
     'opts': ['They lower the cost of finding, negotiating, and completing trades',
              "They produce the physical goods that farmers and factories can't make",
              'They let buyers avoid paying the opportunity cost of what they buy',
              'They hold prices fixed so that buyers are protected from scarcity'],
     'exp': 'Middlemen buy and sell goods or arrange trades, and they reduce transaction costs: the '
            'time and effort of searching out, negotiating, and completing exchanges. That cost saving '
            'is why people value their services.',
     'why': [None,
             "Middlemen usually don't make physical goods. Their value comes from lowering the cost of "
             'arranging trades, not from production.',
             'Every choice still has an opportunity cost; buyers give up alternatives whenever they '
             'buy. Middlemen lower transaction costs, not opportunity cost in general.',
             "Middlemen don't fix prices or remove scarcity. They create value by making it cheaper "
             'and easier to complete trades.']},
    # id 11
    {'ch': 2,
     'q': 'Which is **not** one of the elements of private property rights?',
     'opts': ['A minimum sale price guaranteed by the government',
              'The right to exclusive use of the property',
              'Legal protection against people who invade it',
              'The right to transfer the property to another'],
     'exp': 'Private property rights involve the right to exclusive use, legal protection against '
            'invaders, and the right to transfer. A government-guaranteed price is not part of '
            'ownership; owners bear the gains and losses from their own choices.',
     'why': [None,
             'Exclusive use is a core element of private property rights; it is what lets the owner '
             'control how the property is used.',
             'Legal protection against invaders is one of the three elements of private property '
             "rights; without it, ownership wouldn't be secure.",
             'The right to transfer is one of the three elements of private property rights; it lets '
             'owners sell or give the property to others.']},
    # id 12
    {'ch': 2,
     'q': 'When two people make a voluntary exchange, what does economic reasoning conclude?',
     'opts': ['Both expect to be better off, or the trade would not take place',
              "One party's gain must be exactly equal to the other party's loss",
              "The party with more bargaining power gains at the other's expense",
              'Neither gains unless new goods are produced as part of the trade'],
     'exp': 'A voluntary exchange happens only if both parties expect to benefit, so mutual gain is '
            'the foundation of trade. Trade creates value by moving goods to people who value them '
            'more.',
     'why': [None,
             'This treats trade as zero-sum, the fallacy the Friedmans warned about. Both sides can '
             'gain because they value the goods differently.',
             'Bargaining power can affect how the gains are split, but in a voluntary trade neither '
             'side agrees unless it expects to be better off.',
             'Trade creates value without new production by moving goods from people who value them '
             'less to people who value them more.']},
    # id 13
    {'ch': 5,
     'q': 'From the standpoint of economic efficiency, an activity should be carried to the point '
          'where:',
     'opts': ['Its marginal benefit equals its marginal cost',
              'Its total benefit is as large as it can possibly be',
              'Its total cost is as small as it can be',
              'Its average benefit equals its average cost'],
     'exp': 'Each unit is worth producing as long as its marginal benefit exceeds its marginal cost, '
            'so net gains are greatest where MB equals MC. Stopping earlier leaves worthwhile units '
            'undone; going further adds units that cost more than they are worth.',
     'why': [None,
             'Maximizing total benefit ignores cost. Pushing that far means producing units whose '
             'marginal cost exceeds their marginal benefit, which lowers net gains.',
             'Total cost is smallest when you do nothing at all. Efficiency weighs costs against '
             'benefits rather than minimizing cost by itself.',
             'Efficiency decisions are made at the margin. Averages can hide that the last units cost '
             'more than they add, so the rule compares marginal, not average, values.']},
    # id 14 (retired)
    {'ch': 5,
     'q': 'When external COSTS (negative externality) are present, the market will produce:',
     'opts': ['Too many units at too low a price',
              'Too few units at too high a price',
              'Too few units at too low a price',
              'The efficient quantity'],
     'exp': 'The supply curve understates the true cost, so output is too high and price too low. '
            'Including all costs shifts supply left (S2): lower Q, higher P.',
     'retired': True},
    # id 15 (retired)
    {'ch': 5,
     'q': 'When external BENEFITS (positive externality) are present, the market will usually produce:',
     'opts': ['Too few units', 'Too many units', 'The efficient quantity', 'Nothing at all'],
     'exp': 'The demand curve understates the total value, so units worth more than they cost may not '
            'get produced. Counting all benefits shifts demand right.',
     'retired': True},
    # id 16
    {'ch': 5,
     'q': 'The two characteristics that define a public good are:',
     'opts': ['Nonrival in consumption and nonexcludable',
              'Provided by government and free of charge to users',
              'Rival in consumption and nonexcludable',
              'Nonrival in consumption and excludable'],
     'exp': "A public good can be enjoyed by many people at once without reducing anyone else's use, "
            'so it is nonrival, and it is costly or impossible to keep nonpayers from using it, so it '
            'is nonexcludable.',
     'why': [None,
             'This confuses who supplies a good with what kind of good it is. The text stresses that a '
             "good's characteristics, not the sector producing it, make it public.",
             "Rival means one person's use reduces what others can use. Public goods are the opposite: "
             'many people can enjoy the same unit at the same time.',
             'If nonpayers could be excluded, sellers could charge for the good and the free-rider '
             'problem would largely disappear. Public goods are nonexcludable.']},
    # id 17
    {'ch': 5,
     'q': 'A person who enjoys the benefits of a good without helping pay for its cost is called a:',
     'opts': ['Free rider', 'Rent seeker', 'Repeat purchaser', 'Third party'],
     'exp': "A free rider receives a good's benefits without helping pay for its cost. When many "
            'people free ride, too little of the good is produced, which is the central problem with '
            'public goods.',
     'why': [None,
             'A rent seeker uses the political process to redirect income toward himself. That is '
             'lobbying for favors, not enjoying a good that others paid for.',
             'A repeat purchaser buys an item often from the same seller and pays each time. The idea '
             'belongs to the discussion of information problems, not to avoiding payment.',
             'A third party is someone outside a transaction who is affected by it, as with '
             "externalities. The specific term for enjoying a good's benefits while dodging its cost "
             'is free rider.']},
    # id 18
    {'ch': 5,
     'q': 'Which of the following is **not** one of the four reasons the invisible hand may fail?',
     'opts': ['Rent seeking', 'Poor information', 'Public goods', 'Lack of competition'],
     'exp': 'The four reasons the invisible hand may fail are lack of competition, externalities, '
            'public goods, and poor information. Rent seeking is not a market failure; it is a source '
            'of government failure.',
     'why': [None,
             'Poor information is one of the four: goods that are hard to evaluate and seldom bought '
             'repeatedly from the same seller can leave customers unhappy.',
             "Public goods are one of the four: because nonpayers can't be excluded, people free ride "
             'and markets tend to supply too little.',
             'Lack of competition is one of the four: sellers who can restrict output and raise prices '
             'cause too few units to be produced.']},
    # id 19 (retired)
    {'ch': 5,
     'q': 'When competition is absent, sellers tend to:',
     'opts': ['Restrict output and raise prices',
              'Expand output and lower prices',
              'Produce the efficient quantity',
              'Create external benefits'],
     'exp': 'Restricted supply (S2) gives Q2 < Q1 and P2 > P1: too few units at too high a price.',
     'retired': True},
    # id 20
    {'ch': 5,
     'q': 'A legal system that enforces contracts and settles disputes between parties is part of '
          "government's:",
     'opts': ['Protective function',
              'Productive function',
              'Regulatory function',
              'Redistributive function'],
     'exp': 'The protective function covers protecting people and their property, including a legal '
            'structure that enforces contracts and a mechanism for settling disputes. A court system '
            'is exactly that.',
     'why': [None,
             'The productive function supplies goods that are hard to provide through markets. '
             "Enforcing contracts protects people's property and agreements, so it belongs to the "
             'protective function.',
             "The text divides government's role into two functions, protective and productive. A "
             'separate regulatory function is not one of them, and contract enforcement fits the '
             'protective one.',
             'Redistribution moves income from some people to others, as with transfer payments. A '
             'court enforcing contracts protects agreements rather than reallocating income.']},
    # id 21
    {'ch': 6,
     'q': 'Because a single vote is very unlikely to decide an election, most voters spend little '
          'effort learning about issues and candidates. This is the:',
     'opts': ['Rational ignorance effect',
              'Special interest effect',
              'Shortsightedness effect',
              'Bundle-purchase problem'],
     'exp': 'Getting informed is costly, and one vote is very unlikely to decide an election, so it is '
            'rational for most voters to stay uninformed on many issues. That is the rational '
            'ignorance effect.',
     'why': [None,
             'The special interest effect is about concentrated benefits and widespread costs. It '
             'feeds on voter inattention, but the inattention itself is rational ignorance.',
             'Shortsightedness concerns policies with clear current benefits and hard-to-see future '
             "costs. It doesn't explain why voters skip learning about issues.",
             "The bundle-purchase problem is that voters must accept a candidate's whole package of "
             "positions. It limits voters' influence but isn't about choosing to stay uninformed."]},
    # id 22
    {'ch': 6,
     'q': 'Representative government is biased toward adopting counterproductive projects when:',
     'opts': ['Benefits are concentrated and costs are widespread',
              'Benefits are widespread and costs are concentrated',
              'Benefits and costs are both widely spread out',
              'Benefits and costs both fall on a small group'],
     'exp': 'When a small group gains a lot and the cost is spread thinly over many voters, the '
            'winners push hard while the losers barely notice, so even counterproductive projects tend '
            'to pass.',
     'why': [None,
             'This is the reverse pattern, Type 4. The few who bear concentrated costs fight hard, so '
             'the bias runs toward rejecting productive projects, not adopting bad ones.',
             'When benefits and costs are both widespread, voting tends to adopt productive projects '
             'and reject unproductive ones, so there is no built-in bias.',
             'When both fall on small groups, each side has a strong stake and stays informed, so '
             'representative government tends to reach the efficient result.']},
    # id 23 (retired)
    {'ch': 6,
     'q': 'Road project: benefits are Adams $20, Chan $12, Green $4, Lee $2, Diaz $2 (total $40). '
          'Under Plan A everyone pays $5 tax. What happens in a majority vote?',
     'opts': ["It fails 3 to 2, even though it's efficient",
              'It passes 3 to 2',
              'It passes unanimously',
              "It fails unanimously because it's inefficient"],
     'exp': 'Only Adams and Chan gain more than $5. Green, Lee, Diaz vote no, so it fails 3-2 even '
            'though total benefits ($40) exceed costs ($25). Under Plan B (taxes proportional to '
            'benefits) it passes unanimously.',
     'retired': True},
    # id 24
    {'ch': 6,
     'q': "Two legislators agree to vote for each other's district projects so that both bills pass. "
          'This practice is called:',
     'opts': ['Logrolling', 'Rent seeking', 'Crony capitalism', 'Rational ignorance'],
     'exp': "Logrolling is vote trading: each legislator supports the other's project in return for "
            'support on their own. It strengthens the special interest effect.',
     'why': [None,
             'Rent seeking is the broader effort to reshape policy so income flows to oneself. '
             "Legislators swapping votes on each other's bills has its own name.",
             'Crony capitalism is resource allocation driven by political favors to businesses. It '
             "isn't the specific practice of legislators trading votes.",
             'Rational ignorance describes voters choosing not to become informed. It has nothing to '
             'do with how legislators trade support.']},
    # id 25 (retired)
    {'ch': 6,
     'q': 'Why do politicians find debt financing attractive, according to public choice analysis?',
     'opts': ['The shortsightedness effect: current benefits now, hard-to-see costs later',
              'The rational ignorance effect makes debt free',
              'Debt-financed projects are always efficient',
              'Bureaucrats prefer smaller budgets'],
     'exp': 'Shortsightedness effect: bias toward clearly defined current benefits with future costs '
            'that are hard to identify.',
     'retired': True},
    # id 26
    {'ch': 6,
     'q': 'Efforts by individuals and interest groups to restructure public policy so more income '
          'flows to themselves are called:',
     'opts': ['Rent seeking', 'Logrolling', 'Pork-barrel spending', 'Shortsightedness'],
     'exp': 'Rent seeking is using the political process to restructure policy so more income flows to '
            'oneself. It diverts resources away from productive activities.',
     'why': [None,
             "Logrolling is one tactic legislators use, trading votes to pass each other's projects. "
             'The general effort to redirect income through policy is rent seeking.',
             'Pork-barrel spending is a kind of legislation that funds local projects. The term for '
             'groups working to redirect income through policy is rent seeking.',
             'Shortsightedness is the political bias toward current benefits with hidden future costs, '
             'not the efforts of groups to redirect income to themselves.']},
    # id 27
    {'ch': 6,
     'q': 'The bootlegger-and-Baptist strategy describes:',
     'opts': ['Self-interested favor seeking packaged as moral behavior',
              'Moral reformers and business groups openly splitting a subsidy',
              'Voters trading support across unrelated moral issues',
              'Regulators siding with consumers against large firms'],
     'exp': 'Opportunistic rent seekers frame their programs around popular goals, such as child '
            'safety or saving family farms, to win support from idealists, while the real payoff is '
            'government favoritism.',
     'why': [None,
             "The point is that the self-interest is disguised. The idealists usually don't realize "
             'they are helping a special interest, so nothing is openly split.',
             'Trading support across issues is logrolling, which legislators do. The '
             'bootlegger-and-Baptist idea is about disguising favor seeking as a moral cause.',
             'It works the other way: the strategy helps well-organized interests win favors, often at '
             "consumers' expense, while looking like a public-spirited cause."]},
    # id 28 (retired)
    {'ch': 6,
     'q': 'The U.S. sugar program (concentrated gains for ~20,000 growers, ~$25 cost per household) '
          'illustrates:',
     'opts': ['The special interest effect',
              'The rational ignorance effect only',
              'A public good',
              'An efficient government program'],
     'exp': 'Large personal benefit for a few + small individual cost spread over many = special '
            "interest effect. The program persists even though it's counterproductive.",
     'retired': True},
    # id 29
    {'ch': 6,
     'q': 'Which of the following is a source of **government** failure rather than market failure?',
     'opts': ['Weak incentives for operational efficiency',
              'External costs that markets fail to register',
              'Public goods that invite many free riders',
              'Sellers restricting output to raise prices'],
     'exp': 'Weak incentives for operational efficiency is one of the four sources of government '
            'failure, along with the special interest effect, the shortsightedness effect, and rent '
            'seeking.',
     'why': [None,
             "External costs are one of the four sources of market failure: the market doesn't "
             'register costs imposed on others. They are not a source of government failure.',
             "Public goods are a source of market failure: since nonpayers can't be excluded, people "
             'free ride and markets supply too little.',
             'Sellers restricting output to raise prices reflects a lack of competition, which the '
             'text lists as a source of market failure.']},
    # id 30
    {'ch': 7,
     'q': 'A furniture maker buys lumber and uses it to build tables sold to households. Why does GDP '
          "leave out the furniture maker's purchase of the lumber?",
     'opts': ["The lumber's value is already part of the price of the finished table",
              'Lumber sold between two businesses is counted under net exports instead',
              "The furniture maker's purchase is counted as a government purchase",
              'Business-to-business sales are recorded separately in national income'],
     'exp': 'The lumber is an intermediate good: its value is embodied in the final price of the '
            'table. Counting the lumber sale and the table sale would count the same lumber twice, so '
            'only the final-user good is summed.',
     'why': [None,
             'Net exports cover sales between domestic buyers and foreign buyers. A lumber sale '
             'between two domestic businesses involves no foreign trade at all; it is simply excluded '
             'as an intermediate good.',
             'Government purchases are spending by government on goods and services. A private '
             'furniture maker is not a government, and its input purchases are intermediate goods, '
             'which are left out entirely.',
             'There is no separate account where intermediate sales are added in. National income sums '
             'compensation, self-employment income, rents, interest, and profits; it does not add '
             'business-to-business purchases of inputs.']},
    # id 31
    {'ch': 7,
     'q': 'Which item belongs in the resource cost-income approach to GDP rather than in the '
          'expenditure approach?',
     'opts': ['Employee compensation',
              'Gross private investment',
              'Exports minus imports',
              'Government purchases'],
     'exp': 'The resource cost-income approach adds up costs and incomes from production: employee '
            'compensation, self-employment income, rents, interest, and corporate profits (plus '
            'indirect costs). Employee compensation is the largest of these income components.',
     'why': [None,
             'Gross private investment is spending on final goods such as new machines, buildings, and '
             'inventories, so it is one of the four expenditure components, not an income payment to a '
             'resource supplier.',
             'Exports minus imports is net exports, the spending of foreigners on domestic output, net '
             'of imports. It is one of the four expenditure-approach components, not an income '
             'component.',
             'Government purchases are spending on final goods and services by governments, one of the '
             'four expenditure components. Paying for output is spending; the resource cost-income '
             'side records the wages and profits it generates.']},
    # id 32 (retired)
    {'ch': 7,
     'q': 'Nominal GDP is $27,361 billion and the GDP deflator is 122.3 (base year = 100). Real GDP in '
          'base-year dollars is about:',
     'opts': ['$22,372 billion', '$33,463 billion', '$27,361 billion', '$24,950 billion'],
     'exp': 'Real GDP = Nominal GDP / (Deflator / 100) = 27,361 / 1.223 = about 22,372. (The 2023 '
            'figure in 2017 dollars from your slides.)',
     'retired': True},
    # id 33
    {'ch': 7,
     'q': 'What is the main difference in coverage between the GDP deflator and the consumer price '
          'index?',
     'opts': ['The deflator covers the whole GDP bundle; the CPI tracks household purchases',
              'The CPI covers the whole GDP bundle; the deflator tracks household purchases',
              'The deflator tracks capital goods; the CPI tracks consumer services instead',
              'Both use one identical basket but are published by different agencies'],
     'exp': 'The GDP deflator is the broader index: it measures prices of the whole market basket '
            'included in GDP. The CPI measures only the cost of the typical bundle of goods and '
            'services households buy.',
     'why': [None,
             'This reverses the two indexes. The CPI is the better-known index, but it covers only '
             'household purchases; the deflator is the one built on everything in GDP.',
             'The deflator is not limited to capital goods; it covers everything in GDP, consumer '
             'goods included. And the CPI tracks household purchases of goods and services, not '
             'services only.',
             'The two indexes use different market baskets: the whole GDP bundle versus the household '
             'bundle. That is why they can move differently, even though their inflation estimates are '
             'usually similar.']},
    # id 34
    {'ch': 7,
     'q': 'Which of these activities adds nothing to measured GDP?',
     'opts': ['A parent cooking dinner every night for the family',
              'A family paying a personal chef to prepare their meals',
              'A restaurant buying a new commercial oven for its kitchen',
              'A city government paving a neighborhood street'],
     'exp': 'Household production is excluded because no market transaction takes place. A parent '
            'cooking for the family produces real value, but nothing is bought or sold, so GDP does '
            'not record it.',
     'why': [None,
             'Paying a personal chef is a market purchase of a final service, so it counts as '
             'consumption. The same meals count when bought in a market and are left out only when '
             'produced at home.',
             'A new oven bought by a restaurant is a final capital good, counted as gross private '
             'investment. It is not an intermediate good, because it is not used up in a single '
             'production stage.',
             'Paving a street is a government purchase of a final good, one of the four expenditure '
             'components, so it adds to GDP.']},
    # id 35
    {'ch': 7,
     'q': 'A hurricane wrecks homes and roads, and a large rebuilding effort follows. How is GDP '
          'affected?',
     'opts': ['No deduction is made for the damage, while rebuilding spending is added',
              'The damage is subtracted from GDP, while the rebuilding spending is added',
              'The damage is subtracted from GDP, and rebuilding spending is left out',
              'Neither the damage nor the rebuilding spending changes measured GDP'],
     'exp': 'GDP measures current production and makes no adjustment for destruction by nature, so the '
            'hurricane damage is never subtracted. The rebuilding is new production, so that spending '
            'is added to GDP.',
     'why': [None,
             'GDP has no entry that subtracts lost wealth or destroyed property. It only adds the '
             'market value of current production, so the damage is not deducted.',
             'Two errors: the damage is not subtracted, because GDP ignores destruction; and '
             'rebuilding is current production of final goods and services, so it is counted.',
             'Rebuilding homes and roads is new production purchased by households, firms, and '
             'governments, so it does change GDP. Only the damage side is ignored.']},
    # id 36 (retired)
    {'ch': 7,
     'q': 'Between 2017 and 2023, nominal GDP rose 39.5%, but real GDP rose only 14.1%. Why?',
     'opts': ['Prices rose about 22% over the period',
              'Population fell',
              'Net exports were negative',
              'Intermediate goods were excluded'],
     'exp': 'Nominal growth mixes higher output with higher prices. Deflating removes the price '
            'increase (deflator went 100 to 122.3).',
     'retired': True},
    # id 37 (retired)
    {'ch': 8,
     'q': 'Population age 16+ = 250M, employed = 152M, unemployed = 8M. What is the UNEMPLOYMENT rate?',
     'opts': ['5.0%', '3.2%', '5.3%', '64%'],
     'exp': 'Unemployment rate = unemployed / labor force. Labor force = 152 + 8 = 160M, so 8/160 = '
            '5%. (Dividing by population is a common trap.)',
     'retired': True},
    # id 38 (retired)
    {'ch': 8,
     'q': 'Same economy: population 16+ = 250M, employed = 152M, unemployed = 8M. What is the LABOR '
          'FORCE PARTICIPATION rate?',
     'opts': ['64%', '60.8%', '95%', '5%'],
     'exp': 'LFPR = labor force / population 16+ = 160 / 250 = 64%. (152/250 = 60.8% is the '
            'employment-population ratio.)',
     'retired': True},
    # id 39
    {'ch': 8,
     'q': 'Dana works 20 hours a week for pay at a bookstore and spends her evenings applying for '
          'full-time jobs. How is she classified?',
     'opts': ['Employed', 'Unemployed', 'Not in the labor force', 'Cyclically unemployed'],
     'exp': 'Anyone 16 or older working for pay at least one hour per week counts as employed. Dana '
            'works 20 paid hours, so she is employed even though she wants a full-time job.',
     'why': [None,
             'The unemployed category is only for people not currently employed. Searching for a '
             'better job does not make a person with a paid job unemployed.',
             'People not in the labor force are neither working nor seeking work. Dana both works and '
             'searches, so she is clearly in the labor force.',
             'Cyclical unemployment is a type of unemployment caused by a downturn. Dana has a paid '
             'job, so she is not unemployed of any type.']},
    # id 40 (retired)
    {'ch': 8,
     'q': "A full-time college student who isn't working or looking for work is:",
     'opts': ['Not in the labor force', 'Unemployed', 'Employed', 'Frictionally unemployed'],
     'exp': 'Not working and not seeking work = not in the labor force (same for retirees and '
            'homemakers).',
     'retired': True},
    # id 41
    {'ch': 8,
     'q': 'An auto worker is laid off for two weeks while the plant retools and spends the time on '
          'vacation, expecting to be called back. How is he classified?',
     'opts': ['Unemployed', 'Employed', 'Not in the labor force', 'Self-employed'],
     'exp': 'A person on layoff waiting to return to a previous job is counted as unemployed, even '
            'without searching for other work. The vacation does not change his layoff status.',
     'why': [None,
             'He is not working for pay during the layoff, so he does not meet the employed '
             'definition. Expecting to be recalled is exactly the layoff rule for the unemployed.',
             'Not in the labor force is for people neither employed nor counted as unemployed, such as '
             'retirees and students. The layoff rule keeps him in the labor force.',
             'Self-employed people work for themselves. He is a laid-off employee of the plant and is '
             'not working at all during the layoff.']},
    # id 42
    {'ch': 8,
     'q': 'What is the underlying cause of frictional unemployment?',
     'opts': ['Imperfect information about available workers and available jobs',
              'A mismatch between the skills workers have and those jobs require',
              'A general decline in business activity during a downturn',
              'Too few total jobs for everyone who would like to work'],
     'exp': 'Frictional unemployment comes from imperfect information: employers are not aware of all '
            'available workers, and workers are not aware of all available jobs, so matching takes '
            'time.',
     'why': [None,
             "A mismatch between workers' skills and job requirements is structural unemployment. "
             'Better information would not fix it, because the workers still lack the skills.',
             'A general decline in business activity causes cyclical unemployment, which rises in '
             'downturns. Frictional unemployment exists even in good times.',
             'Too few total jobs is not the cause of frictional unemployment; jobs exist but workers '
             'and employers have not yet found each other.']},
    # id 43
    {'ch': 8,
     'q': 'New production technology sharply cuts the demand for workers with certain skills. Job '
          'openings exist, but they call for skills the laid-off workers lack. What type of '
          'unemployment is this?',
     'opts': ['Structural unemployment',
              'Frictional unemployment',
              'Cyclical unemployment',
              'Seasonal unemployment'],
     'exp': 'New technology changed the relative demand for skills, and the openings require skills '
            'the laid-off workers lack. That is structural unemployment.',
     'why': [None,
             'Frictional unemployment is about imperfect information. Here the workers know about the '
             'openings but cannot fill them, so more information would not help.',
             'Cyclical unemployment comes from a general downturn in business activity. Nothing here '
             'describes a recession; the cause is a change in technology.',
             'Seasonal swings are not the cause here. The jobs disappeared because technology '
             'permanently changed which skills firms need.']},
    # id 44
    {'ch': 8,
     'q': 'Which describes an economy operating at full employment?',
     'opts': ['Frictional and structural unemployment remain, but cyclical does not',
              'Cyclical and frictional unemployment remain, but structural does not',
              'The unemployment rate is zero because everyone who wants a job has one',
              'Actual GDP is below potential GDP because some workers are still idle'],
     'exp': 'Full employment is the level at which unemployment is normal given frictional and '
            'structural factors. Only cyclical unemployment is absent, so the unemployment rate equals '
            'the natural rate.',
     'why': [None,
             'Cyclical unemployment is the part that disappears at full employment. Structural '
             'unemployment is part of the normal, natural rate and remains.',
             'Full employment does not mean zero unemployment. Job shopping and skill mismatches '
             'continue, so frictional and structural unemployment remain.',
             'At full employment, actual GDP equals potential GDP. Actual output below potential '
             'describes a recession, with unemployment above the natural rate.']},
    # id 45 (retired)
    {'ch': 8,
     'q': 'During a recession, which is true?',
     'opts': ['Actual GDP is below potential GDP',
              'Actual unemployment is below the natural rate',
              'Employment exceeds full employment',
              'Cyclical unemployment is zero'],
     'exp': 'In a recession, actual unemployment rises above the natural rate and actual GDP falls '
            'below potential.',
     'retired': True},
    # id 46 (retired)
    {'ch': 8,
     'q': 'The CPI was 150 at the end of last year and 157.5 at the end of this year. The inflation '
          'rate was:',
     'opts': ['5%', '7.5%', '4.8%', '57.5%'],
     'exp': 'Inflation = (157.5 - 150) / 150 x 100 = 7.5 / 150 = 5%.',
     'retired': True},
    # id 47 (retired)
    {'ch': 8,
     'q': 'People expected 3% inflation, but prices rose 7%. This is:',
     'opts': ['Inflation higher than anticipated (unanticipated inflation)',
              'Anticipated inflation',
              'Inflation lower than anticipated',
              'Deflation'],
     'exp': 'Actual exceeded expected, so 4 points of it was a surprise. Unanticipated inflation is '
            'what disrupts long-term contracts.',
     'retired': True},
    # id 48
    {'ch': 8,
     'q': 'Starting from the high point, which sequence lists the business cycle phases in the order '
          'they occur?',
     'opts': ['Peak, contraction, recessionary trough, expansion',
              'Peak, recessionary trough, contraction, expansion',
              'Peak, expansion, recessionary trough, contraction',
              'Peak, contraction, expansion, recessionary trough'],
     'exp': 'After a peak, business conditions slow and the contraction begins. The contraction '
            'bottoms out at the recessionary trough, and expansion follows back toward the next peak.',
     'why': [None,
             'The contraction is the decline that leads to the trough, so it must come before the '
             'trough, not after it.',
             'Expansion is the rising phase that leads to a peak, so it cannot come right after the '
             'peak. Output falls first.',
             'The trough is the bottom of the contraction, so it comes before the expansion. Here '
             'expansion is placed before the economy has hit bottom.']},
    # id 49
    {'ch': 8,
     'q': 'Which of these is **not** one of the reasons high and variable inflation harms an economy?',
     'opts': ['It makes the payoff on long-term contracts easier to forecast',
              'It distorts the information that relative prices deliver',
              'It raises the risk of long-term projects and slows investment',
              'It shifts effort from producing toward protecting wealth'],
     'exp': 'High inflation is nearly always highly variable and hard to predict, so it makes '
            'long-term contract outcomes harder, not easier, to forecast. The other three are listed '
            'harms.',
     'why': [None,
             'Distorting the information prices deliver is one of the listed harms: firms and '
             'consumers mistake general price rises for changes in relative prices.',
             'Higher risk and less investment is a listed harm: unanticipated inflation alters the '
             'outcomes of long-term projects like buying a machine.',
             'This is a listed harm: people spend less time producing and more time protecting their '
             "wealth and income from inflation's uncertainty."]},
    # id 50
    {'ch': 9,
     'q': 'Economists give three reasons the aggregate demand curve slopes downward. Which of the '
          'following is **not** one of them?',
     'opts': ["A lower price level narrows firms' profit margins, so they cut output",
              'A lower price level raises the purchasing power of a fixed money supply',
              'A lower price level reduces money demand and lowers the real interest rate',
              'A lower price level makes domestic goods cheaper relative to foreign goods'],
     'exp': 'The profit-margin argument belongs to supply: it explains why SRAS slopes upward when '
            'prices rise unexpectedly. It says nothing about why buyers purchase more at a lower price '
            'level, so it is not one of the three AD reasons.',
     'why': [None,
             'This is one of the three AD reasons: a lower price level lets the fixed quantity of '
             'money buy more, so purchases rise.',
             'This is a genuine AD reason: a lower price level reduces the demand for money, lowers '
             'the real interest rate, and stimulates current purchases.',
             'This is the international AD reason: other things constant, a lower price level makes '
             'domestic goods cheaper relative to foreign goods, so buyers purchase more of them.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD'}],
             'points': [{'at': [35, 65], 'label': 'A'}, {'at': [60, 40], 'label': 'B'}],
             'guides': True,
             'xticks': [[35, 'Y1'], [60, 'Y2']],
             'yticks': [[40, 'P2'], [65, 'P1']],
             'alt': 'A downward-sloping AD curve. Point A is at the higher price level P1 and output '
                    'Y1; point B is at the lower price level P2 and the larger output Y2.'}},
    # id 51
    {'ch': 9,
     'q': 'Why is the long-run aggregate supply (LRAS) curve vertical at the full-employment output '
          'rate?',
     'opts': ['A higher price level does not loosen limits set by resources, technology, and '
              'institutions',
              'Resource prices stay fixed by long-term contracts, so firms are unable to change output',
              'Buyers purchase the same total quantity of goods regardless of the price level',
              'Firms earn higher profits at higher price levels and reinvest them to grow their '
              'output'],
     'exp': 'Full-employment output YF is set by the resource base, technology, and the efficiency of '
            'institutions, and a higher price level changes none of them. So a higher price level '
            'cannot produce a sustainable expansion in output, and LRAS is vertical at YF.',
     'why': [None,
             'Contracts that fix resource prices describe the **short** run. LRAS shows output after '
             'people have had time to adjust their commitments, so contracts cannot explain its shape.',
             'This mixes up supply with demand. LRAS is about how much the economy can produce on a '
             'sustained basis, not how much buyers purchase at each price level.',
             'Higher profits from a higher price level are a short-run SRAS story; they fade once '
             'costs catch up and do not change resources, technology, or institutions.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD'},
                       {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS'},
                       {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
             'points': [{'at': [50, 50], 'label': 'E'}],
             'guides': True,
             'xticks': [[50, 'YF']],
             'yticks': [[50, 'P1']],
             'alt': 'A downward-sloping AD curve, an upward-sloping SRAS curve, and a vertical LRAS '
                    'line all pass through point E at full-employment output YF and price level P1.'}},
    # id 52
    {'ch': 9,
     'q': 'In the short run, why do firms supply a larger quantity of output when the price level '
          'rises unexpectedly?',
     'opts': ['Many input costs are locked in by prior contracts, so profit margins widen',
              "The higher price level expands the economy's resource base and technology",
              'Households buy more goods because a higher price level raises their wealth',
              'Firms foresaw the rise and had already built it into their wage contracts'],
     'exp': 'Wages and other resource prices are set by earlier contracts, so when product prices rise '
            'unexpectedly, revenues rise faster than costs. Wider profit margins lead firms to expand '
            'output, which gives SRAS its upward slope.',
     'why': [None,
             'A higher price level does not change resources or technology; those determine LRAS. The '
             'short-run output gain comes from wider profit margins, not new capacity.',
             'This is a demand-side story, and it is backward: a higher price level reduces the '
             'purchasing power of money, lowering real wealth. The question asks why firms supply '
             'more, which comes from contract-fixed costs.',
             'If the rise were foreseen and built into wage contracts, costs would rise along with '
             'prices, margins would not widen, and firms would have no reason to expand.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS'}],
             'points': [{'at': [40, 40], 'label': 'A'}, {'at': [60, 60], 'label': 'B'}],
             'guides': True,
             'xticks': [[40, 'Y1'], [60, 'Y2']],
             'yticks': [[40, 'P1'], [60, 'P2']],
             'alt': 'An upward-sloping SRAS curve. Point A is at price level P1 and output Y1; point B '
                    'is at the higher price level P2 and the larger output Y2.'}},
    # id 53 (retired)
    {'ch': 9,
     'q': 'The money interest rate is 11% and expected inflation is 5%. The real interest rate is:',
     'opts': ['6%', '16%', '11%', '2.2%'],
     'exp': 'Real interest rate = money interest rate - inflationary premium = 11% - 5% = 6%.',
     'retired': True},
    # id 54 (retired)
    {'ch': 9,
     'q': 'If actual inflation turns out HIGHER than anticipated:',
     'opts': ['Borrowers gain at the expense of lenders',
              'Lenders gain at the expense of borrowers',
              'Neither gains, since the interest rate adjusts',
              'Both gain equally'],
     'exp': 'Borrowers repay with dollars worth less than expected. If inflation is LOWER than '
            'anticipated, lenders gain. Correctly anticipated inflation favors neither.',
     'retired': True},
    # id 55
    {'ch': 9,
     'q': 'A firm issued bonds last year paying a fixed 4% interest rate. If interest rates on newly '
          'issued bonds rise to 6%, what happens to the market price of the older bonds?',
     'opts': ["It falls, because the old bonds' fixed payments are now less attractive to buyers",
              'It rises, because higher interest rates raise the value of interest-paying assets',
              'It stays the same, because the issuer still owes the original fixed payments',
              'It rises, because holders of the old bonds will now receive the new 6% rate'],
     'exp': 'The old bonds keep paying their fixed 4% rate. With new bonds paying 6%, buyers will take '
            'the old bonds only at a lower price, so market interest rates and the prices of '
            'previously issued bonds move in opposite directions.',
     'why': [None,
             'This reverses the relationship. Higher market rates make older, lower-rate bonds less '
             'attractive, so their prices fall rather than rise.',
             'The fixed payments are exactly why the price must change: buyers compare the old 4% '
             'payments with new 6% bonds and will pay less for the old ones.',
             "A bond's interest rate is fixed when it is issued. Holders of the old bonds keep "
             'receiving 4%; they do not get the new 6% rate.']},
    # id 56
    {'ch': 9,
     'q': "A country's exchange rate is determined by market forces, and it runs a trade deficit. What "
          'must be true of its capital flows?',
     'opts': ['Capital inflow exceeds capital outflow, so there is a net inflow of capital',
              'Capital outflow exceeds capital inflow, so there is a net outflow of capital',
              'Capital inflow equals capital outflow, since the exchange rate clears the market',
              'The government must run a budget surplus to pay for the extra imports'],
     'exp': 'In foreign exchange equilibrium, imports − exports = capital inflow − capital outflow. A '
            'trade deficit makes the left side positive, so the country must have a net inflow of '
            'capital.',
     'why': [None,
             'A net capital outflow goes with a trade **surplus**. The trade balance and net capital '
             'inflow have matching signs, so a deficit means net inflow.',
             'The exchange rate balances imports plus capital outflow against exports plus capital '
             'inflow as totals. With imports above exports, inflow must exceed outflow.',
             'The government budget does not appear in the foreign exchange equation. A trade deficit '
             'is matched by a net inflow of capital from foreigners.']},
    # id 57
    {'ch': 9,
     'q': 'When the economy is in long-run equilibrium, which pair of conditions holds?',
     'opts': ['Actual price level equals the anticipated level; unemployment equals the natural rate',
              'Actual price level exceeds the anticipated level; unemployment is below the natural '
              'rate',
              'Actual price level equals the anticipated level; the unemployment rate is zero',
              'Output equals potential GDP; frictional and structural unemployment have disappeared'],
     'exp': 'Long-run equilibrium requires that people correctly anticipated the price level when they '
            'made their agreements. Output then equals potential GDP, and the actual unemployment rate '
            'equals the natural rate.',
     'why': [None,
             'A price level above what people anticipated describes a short-run boom with output above '
             'potential, not a long-run equilibrium.',
             'The price-level half is right, but unemployment does not fall to zero. At full '
             'employment the actual rate equals the natural rate, which includes frictional and '
             'structural unemployment.',
             'Output does equal potential GDP, but frictional and structural unemployment remain; only '
             'cyclical unemployment is absent in long-run equilibrium.']},
    # id 58 (retired)
    {'ch': 9,
     'q': 'An unanticipated increase in the price level will, in the short run:',
     'opts': ['Expand output and employment',
              'Reduce output and employment',
              'Have no effect on output',
              'Permanently increase potential GDP'],
     'exp': 'Real wages and other contracted costs lag, so profits rise and firms expand. In the long '
            'run, costs catch up and output returns to potential.',
     'retired': True},
    # id 59 (retired)
    {'ch': 9,
     'q': 'Using government taxation and spending to achieve macroeconomic goals is:',
     'opts': ['Fiscal policy', 'Monetary policy', 'Trade policy', 'Rent seeking'],
     'exp': 'Fiscal = taxes and spending. Monetary = control of the money supply and credit '
            'conditions.',
     'retired': True},
    # id 60
    {'ch': 9,
     'q': 'A city government sells bonds to savers to pay for a new water treatment plant. In which of '
          'the four key macroeconomic markets is this transaction coordinated?',
     'opts': ['Loanable funds market',
              'Resource market',
              'Goods and services market',
              'Foreign exchange market'],
     'exp': 'Bonds are IOUs, so selling them is borrowing. The loanable funds market coordinates the '
            'actions of borrowers and lenders, with the interest rate bringing them into balance.',
     'why': [None,
             'The resource market is where firms buy labor and other factors of production. Here the '
             'city is borrowing from savers, not hiring resources.',
             'Building the plant will later involve buying goods and services, but the bond sale '
             "itself channels savers' funds to a borrower.",
             'The foreign exchange market coordinates trading one currency for another. Nothing in '
             'this transaction involves exchanging dollars for foreign currency.']},
    # id 61 (retired)
    {'ch': 9,
     'q': 'Are trade deficits necessarily bad?',
     'opts': ['It depends on whether the borrowed funds go to productive investment',
              'Yes, always',
              'No, never',
              'Only when the exchange rate is fixed'],
     'exp': 'A trade deficit reflects capital inflow (borrowing from foreigners). Productive '
            'investment raises future income; funding consumption or unproductive uses lowers it.',
     'retired': True},
    # id 62
    {'ch': 10,
     'q': 'According to the AD–AS model, which of the following would shift the aggregate demand curve '
          'to the right?',
     'opts': ["A decline in the exchange rate value of the nation's currency",
              'An increase in the real interest rate on loans to business firms',
              'A shift toward pessimism about future economic conditions',
              'A decrease in resource prices that lowers production costs'],
     'exp': 'A lower exchange rate value of the currency makes domestic goods cheaper for foreigners '
            'and imports pricier at home, so people buy more domestic output at every price level: AD '
            'shifts to the right.',
     'why': [None,
             'The direction is reversed: a higher real interest rate makes borrowing costlier and '
             'shifts AD to the **left**.',
             'Pessimism about future conditions makes households and businesses spend less, which '
             'shifts AD to the left, not the right.',
             'Lower resource prices reduce production costs, which shifts SRAS to the right. They are '
             'a supply shifter, not an AD shifter.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD1'},
                       {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS1'},
                       {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
             'points': [{'at': [50, 50], 'label': 'E1'}],
             'guides': True,
             'xticks': [[50, 'YF']],
             'yticks': [[50, 'P1']],
             'alt': "The economy's starting position: a downward-sloping AD1 curve, an upward-sloping "
                    'SRAS1 curve, and a vertical LRAS line all pass through E1 at full-employment '
                    'output YF and price level P1. No curve has shifted yet.'},
     'expFig': {'type': 'graph',
                'x': 'Real GDP',
                'y': 'Price level',
                'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'm', 'label': 'AD1'},
                          {'pts': [[35, 85], [95, 25]], 'cls': 'd', 'label': 'AD2', 'dash': True},
                          {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS1'},
                          {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
                'points': [{'at': [50, 50], 'label': 'E1'}, {'at': [60, 60], 'label': 'E2'}],
                'guides': True,
                'xticks': [[50, 'YF'], [60, 'Y2']],
                'yticks': [[50, 'P1'], [60, 'P2']],
                'arrows': [{'from': [72, 30], 'to': [87, 30]}],
                'alt': 'After the change: AD1 shifts right to AD2 while SRAS1 and LRAS stay put. AD2 '
                       'crosses SRAS1 at E2, at output Y2 above YF and the higher price level P2. An '
                       'arrow points from AD1 toward AD2.'}},
    # id 63 (retired)
    {'ch': 10,
     'q': 'A decline in the exchange rate value of the dollar will tend to:',
     'opts': ['Increase AD, because U.S. goods become cheaper to foreigners',
              'Decrease AD, because imports become cheaper',
              'Shift LRAS to the right',
              'Have no effect on AD'],
     'exp': 'A weaker dollar makes U.S. exports cheaper and imports pricier, so net exports and AD '
            'rise.',
     'retired': True},
    # id 64
    {'ch': 10,
     'q': 'Which of the following would shift **both** the LRAS and SRAS curves to the right?',
     'opts': ['Institutional changes that improve the efficiency of resource use',
              "A season of favorable weather that boosts this year's harvest",
              'A temporary drop in the world price of a key imported resource',
              'A reduction in the expected rate of inflation among most businesses'],
     'exp': "Institutional changes that improve the efficiency of resource use raise the economy's "
            'sustainable output, shifting LRAS to the right, and an LRAS shift moves SRAS in the same '
            'direction.',
     'why': [None,
             'Favorable weather is a temporary supply shock. It shifts SRAS but not LRAS, because one '
             'good season cannot be counted on in the future.',
             "A temporary drop in a key import's price is a favorable supply shock. It shifts SRAS "
             "only; the economy's long-run capacity is unchanged.",
             'Lower expected inflation increases SRAS, but it does not change resources, technology, '
             'or institutions, so LRAS stays where it was.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD1'},
                       {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS1'},
                       {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
             'points': [{'at': [50, 50], 'label': 'E1'}],
             'guides': True,
             'xticks': [[50, 'YF']],
             'yticks': [[50, 'P1']],
             'alt': "The economy's starting position: a downward-sloping AD1 curve, an upward-sloping "
                    'SRAS1 curve, and a vertical LRAS line all pass through E1 at full-employment '
                    'output YF and price level P1. No curve has shifted yet.'},
     'expFig': {'type': 'graph',
                'x': 'Real GDP',
                'y': 'Price level',
                'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD1'},
                          {'pts': [[20, 20], [85, 85]], 'cls': 'm', 'label': 'SRAS1'},
                          {'pts': [[36, 12], [95, 71]], 'cls': 's', 'label': 'SRAS2', 'dash': True},
                          {'pts': [[50, 8], [50, 92]], 'cls': 'm', 'label': 'LRAS1'},
                          {'pts': [[62, 8], [62, 80]], 'cls': 'v', 'label': 'LRAS2', 'dash': True}],
                'points': [{'at': [50, 50], 'label': 'E1'}, {'at': [62, 38], 'label': 'E2'}],
                'guides': True,
                'xticks': [[50, 'YF1'], [62, 'YF2']],
                'yticks': [[38, 'P2'], [50, 'P1']],
                'arrows': [{'from': [52, 70], 'to': [60, 70]}, {'from': [63, 58], 'to': [80, 58]}],
                'alt': 'After the change: LRAS shifts right from LRAS1 at YF1 to LRAS2 at YF2, and '
                       'SRAS shifts right from SRAS1 to SRAS2. AD1 is unchanged and crosses SRAS2 at '
                       'E2 on LRAS2, at the larger output YF2 and the lower price level P2. Arrows '
                       'point from the old curves toward the new ones.'}},
    # id 65
    {'ch': 10,
     'q': "A severe drought cuts this year's crop output, but normal rainfall is expected next year. "
          'How does this affect aggregate supply?',
     'opts': ['SRAS shifts to the left while LRAS stays where it was',
              'Both SRAS and LRAS shift to the left by the same amount',
              'LRAS shifts to the left while SRAS stays where it was',
              'AD shifts to the left as farmers earn less income this year'],
     'exp': "A drought is an unfavorable supply shock. Because it is temporary, it reduces this year's "
            'productive capability and shifts SRAS to the left, while long-run capacity, and therefore '
            'LRAS, is unchanged.',
     'why': [None,
             'LRAS shifts only when resources, technology, or institutions change lastingly. A '
             'one-year drought with normal rain expected next year leaves long-run capacity intact.',
             'This reverses which curve moves. A temporary shock shifts SRAS, and any LRAS shift would '
             'also move SRAS in the same direction.',
             'The drought hits production, so it is a supply shock. The model treats it as a leftward '
             'shift in SRAS, not as a change in AD.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD1'},
                       {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS1'},
                       {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
             'points': [{'at': [50, 50], 'label': 'E1'}],
             'guides': True,
             'xticks': [[50, 'YF']],
             'yticks': [[50, 'P1']],
             'alt': "The economy's starting position: a downward-sloping AD1 curve, an upward-sloping "
                    'SRAS1 curve, and a vertical LRAS line all pass through E1 at full-employment '
                    'output YF and price level P1. No curve has shifted yet.'},
     'expFig': {'type': 'graph',
                'x': 'Real GDP',
                'y': 'Price level',
                'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD1'},
                          {'pts': [[20, 20], [85, 85]], 'cls': 'm', 'label': 'SRAS1'},
                          {'pts': [[10, 30], [70, 90]], 'cls': 's', 'label': 'SRAS2', 'dash': True},
                          {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
                'points': [{'at': [50, 50], 'label': 'E1'}, {'at': [40, 60], 'label': 'E2'}],
                'guides': True,
                'xticks': [[40, 'Y2'], [50, 'YF']],
                'yticks': [[50, 'P1'], [60, 'P2']],
                'arrows': [{'from': [74, 76], 'to': [58, 76]}],
                'alt': 'After the change: SRAS1 shifts left to SRAS2 while AD1 and LRAS stay put. AD1 '
                       'crosses SRAS2 at E2, at output Y2 below YF and the higher price level P2. An '
                       'arrow points from SRAS1 toward SRAS2.'}},
    # id 66 (retired)
    {'ch': 10,
     'q': 'Steady, predictable growth from capital formation and better technology will:',
     'opts': ['Shift LRAS right without disrupting macro equilibrium',
              'Cause a recession',
              'Cause an unsustainable boom',
              'Shift only SRAS'],
     'exp': "Anticipated changes let decision makers adjust ahead of time, so equilibrium isn't "
            'disrupted. Full-employment output rises from YF1 to YF2.',
     'retired': True},
    # id 67 (retired)
    {'ch': 10,
     'q': 'In the SHORT run, an unanticipated increase in AD causes:',
     'opts': ['A higher price level and output above long-run potential',
              'A lower price level and lower output',
              'A higher price level with no change in output',
              'Unemployment above the natural rate'],
     'exp': 'Profit margins temporarily improve, output exceeds potential, and unemployment falls '
            'BELOW the natural rate (e.g., P105 and Y2 on the slide).',
     'retired': True},
    # id 68 (retired)
    {'ch': 10,
     'q': 'In the LONG run, after an unanticipated increase in AD:',
     'opts': ['Resource prices rise, SRAS shifts left, and output returns to potential at a higher '
              'price level',
              'Output stays permanently above potential',
              'Resource prices fall and SRAS shifts right',
              'LRAS shifts right to match the new AD'],
     'exp': 'Contracts get renegotiated, costs rise, SRAS shifts left, and you end at full-employment '
            'output with a higher price level (P110). The demand boost only expanded output '
            'temporarily.',
     'retired': True},
    # id 69 (retired)
    {'ch': 10,
     'q': 'After an unanticipated DECREASE in AD, what eventually returns the economy to long-run '
          'equilibrium?',
     'opts': ['Lower resource prices and lower real interest rates',
              'Higher resource prices and higher real interest rates',
              'A permanent leftward shift of LRAS',
              'Nothing; the economy stays in recession permanently'],
     'exp': 'Weak demand lowers resource prices (SRAS shifts right) and real interest rates fall, '
            'stimulating AD. Output returns to potential at a lower price level (P90), but it can be a '
            'lengthy, painful process.',
     'retired': True},
    # id 70 (retired)
    {'ch': 10,
     'q': 'An unexpected event that temporarily increases or decreases aggregate supply is a:',
     'opts': ['Supply shock', 'Demand shock', 'Fiscal policy', 'Shift in LRAS'],
     'exp': 'Supply shocks catch people by surprise. Examples of negative ones: the 2022 '
            "Russia-Ukraine war's effect on wheat and energy, Hurricane Katrina.",
     'retired': True},
    # id 71 (retired)
    {'ch': 10,
     'q': 'A sharp, unexpected rise in the world price of oil will, in the short run:',
     'opts': ['Shift SRAS left, raising the price level and lowering output',
              'Shift SRAS right, lowering the price level and raising output',
              'Shift AD right, raising both price level and output',
              'Have no effect until LRAS shifts'],
     'exp': 'Higher resource costs shift SRAS left: price level up (P110), output down (Y2). If the '
            'shock is permanent, LRAS shifts left too; if temporary, SRAS eventually moves back.',
     'retired': True},
    # id 72 (retired)
    {'ch': 10,
     'q': 'A temporary bumper crop from good weather would cause:',
     'opts': ['A lower price level and higher current GDP, with LRAS unchanged',
              'A higher price level and lower GDP',
              'A permanent rightward shift in LRAS',
              'A leftward shift in AD'],
     'exp': 'Favorable, temporary supply shock: SRAS shifts right, price level falls (P95), output '
            "rises to Y2. Because it can't be counted on, LRAS stays put.",
     'retired': True},
    # id 73
    {'ch': 10,
     'q': 'Wage contracts and loan agreements in an economy were based on an expected inflation rate '
          'of 5%, but actual inflation turns out to be 2%. How will firms tend to respond?',
     'opts': ['Profits shrink as costs outpace product prices, so firms cut output',
              'Profits grow as costs fall faster than prices, so firms expand output',
              'Output stays at YF, because inflation remained positive at 2%',
              "Firms raise output, because lower inflation increases buyers' wealth"],
     'exp': 'Actual inflation below the expected rate is the equivalent of a fall in the price level '
            'relative to the costs locked into contracts. Product prices rise more slowly than costs, '
            'so firms incur losses and cut output.',
     'why': [None,
             'Costs were locked in at the 5% expected rate, so they keep rising at that pace. Product '
             'prices rising only 2% squeezes margins rather than widening them.',
             'What matters is the gap between actual and expected inflation, not whether inflation is '
             'positive. Inflation 3 points below the expected rate reduces output.',
             "The model works through firms' profit margins: product prices lag the contracted costs, "
             'so firms produce less, not more.']},
    # id 74
    {'ch': 10,
     'q': 'According to the AD–AS model, what are the two causes of recessions?',
     'opts': ['Unanticipated reductions in AD and unfavorable supply shocks',
              'Anticipated reductions in AD and favorable supply shocks',
              'Unanticipated increases in AD and unfavorable supply shocks',
              'Unanticipated reductions in AD and steady, expected growth of LRAS'],
     'exp': 'Recessions occur when prices in the goods and services market are low relative to '
            'resource prices and production costs. That results from unanticipated reductions in AD or '
            'from unfavorable supply shocks.',
     'why': [None,
             'Anticipated changes can be built into contracts ahead of time, so they need not disrupt '
             'equilibrium, and favorable supply shocks cause booms, not recessions.',
             'Unfavorable supply shocks do cause recessions, but unanticipated **increases** in AD '
             'push output above YF and cause booms.',
             'Steady, expected LRAS growth is anticipated and raises sustainable output, so it does '
             'not cause recessions. The second cause is an unfavorable supply shock.']},
    # id 75
    {'ch': 10,
     'q': 'During a recession, what tends to happen to real interest rates, and how does that help the '
          'economy recover?',
     'opts': ['They fall as investment demand weakens, which stimulates AD',
              'They rise as lenders fear defaults, which stimulates saving',
              'They fall as investment demand weakens, which shifts LRAS right',
              'They rise as investment demand weakens, which restrains SRAS'],
     'exp': 'In a recession, weak demand for investment pushes real interest rates down. The lower '
            'rates stimulate AD, which helps direct the economy back toward full employment.',
     'why': [None,
             'The model ties recession interest rates to weak investment demand, which lowers them. '
             'And rates aid recovery by stimulating AD, not by stimulating saving.',
             'Falling rates are right, but they work through demand: lower rates stimulate AD. LRAS '
             'depends on resources, technology, and institutions.',
             'Weak investment demand lowers interest rates rather than raising them, and interest '
             'rates affect AD, not SRAS.']},
    # id 76
    {'ch': 10,
     'q': 'In AD–AS terms, which combination best explains the 2008–2009 recession?',
     'opts': ['Falling housing and stock prices cut AD while soaring energy prices cut SRAS',
              'Rising housing and stock prices cut AD while falling energy prices cut SRAS',
              'Falling housing and stock prices cut LRAS while soaring energy prices cut AD',
              'Falling housing prices raised AD while falling energy prices raised SRAS'],
     'exp': 'Falling housing prices and plunging stock prices reduced wealth and AD, while soaring '
            'energy prices in 2007 and early 2008 were an unanticipated reduction in SRAS. Sinking '
            'confidence then cut AD further.',
     'why': [None,
             'The directions are reversed: rising asset prices raise wealth and AD, and falling energy '
             'prices would increase SRAS. In 2007–2008 asset prices fell and energy prices soared.',
             'This swaps the curves. Asset prices change wealth and so shift AD, while higher energy '
             'prices are a supply shock that shifts SRAS.',
             'Falling housing prices reduced wealth and therefore AD, and energy prices soared rather '
             'than fell, which reduced SRAS.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD1'},
                       {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS1'},
                       {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
             'points': [{'at': [50, 50], 'label': 'E1'}],
             'guides': True,
             'xticks': [[50, 'YF']],
             'yticks': [[50, 'P1']],
             'alt': "The economy's starting position: a downward-sloping AD1 curve, an upward-sloping "
                    'SRAS1 curve, and a vertical LRAS line all pass through E1 at full-employment '
                    'output YF and price level P1. No curve has shifted yet.'},
     'expFig': {'type': 'graph',
                'x': 'Real GDP',
                'y': 'Price level',
                'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'm', 'label': 'AD1'},
                          {'pts': [[8, 72], [68, 12]], 'cls': 'd', 'label': 'AD2', 'dash': True},
                          {'pts': [[20, 20], [85, 85]], 'cls': 'm', 'label': 'SRAS1'},
                          {'pts': [[8, 18], [70, 80]], 'cls': 's', 'label': 'SRAS2', 'dash': True},
                          {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
                'points': [{'at': [50, 50], 'label': 'E1'}, {'at': [35, 45], 'label': 'E2'}],
                'guides': True,
                'xticks': [[35, 'Y2'], [50, 'YF']],
                'yticks': [[45, 'P2'], [50, 'P1']],
                'arrows': [{'from': [68, 30], 'to': [52, 30]}, {'from': [75, 76], 'to': [67, 76]}],
                'alt': 'After the change: AD1 shifts left to AD2 and SRAS1 shifts left to SRAS2, while '
                       'LRAS stays put. AD2 and SRAS2 cross at E2, at output Y2 well below YF and '
                       'price level P2. Arrows point from the original curves toward the new ones.'}},
    # id 77 (retired)
    {'ch': 10,
     'q': 'Which would be MOST likely to throw the U.S. economy into a recession?',
     'opts': ['An unanticipated drop in AD from a sharp decline in consumer confidence',
              'Lower transaction costs from the growth of the Internet',
              'An unanticipated fall in the world price of oil',
              'Steady, anticipated growth in the capital stock'],
     'exp': 'Unanticipated AD reductions cause recessions. Lower transaction costs and cheaper oil '
            'boost supply (cheaper oil hurts oil-producing states, though).',
     'retired': True},
    # id 78
    {'ch': 10,
     'q': 'Over the past six decades of U.S. business cycles, how have the lengths of expansions '
          'compared with the lengths of recessions?',
     'opts': ['Expansions have typically lasted far longer than recessions',
              'Recessions have typically lasted longer than expansions',
              'Expansions and recessions have lasted about equally long',
              'Expansions have grown shorter while recessions lengthened'],
     'exp': 'Over the past six decades, expansions have been far longer than recessions. Several '
            'expansions ran over 100 months, while most recessions lasted about a year or less; even '
            'the severe 2007–2009 recession lasted 18 months.',
     'why': [None,
             'Recessions get a lot of attention, but the record shows they have been brief, mostly '
             'under a year, while expansions have usually run for years.',
             'The lengths are far from equal: expansions such as 1991–2001 at 120 months and 2009–2020 '
             'at 128 months dwarf recessions that lasted under 20 months.',
             'The trend runs the other way: the two longest expansions on record are among the most '
             'recent, while recent recessions were mostly short.']},
    # id 79
    {'ch': 1,
     'q': 'Why are goods scarce, according to the economic approach?',
     'opts': ['People want more of them than nature freely provides',
              'Governments restrict how much firms are allowed to make',
              'Firms produce them with wasteful production methods',
              'Their prices are set too high for most buyers to afford'],
     'exp': "Goods are scarce because people's desire for them far outstrips what nature freely "
            'provides. Scarcity forces choices no matter how prices are set or how well firms and '
            'governments perform.',
     'why': [None,
             'Government limits can make a good harder to get, but scarcity would exist even without '
             'them, because wants exceed what nature provides.',
             "Wasteful methods reduce output, but even perfectly efficient firms couldn't satisfy "
             'every want. Scarcity comes from wants exceeding what nature makes available.',
             'High prices are a result of scarcity, not its cause. Prices are high because people want '
             'more of a good than is available.']},
    # id 80
    {'ch': 1,
     'q': 'In economics, which of these counts as capital?',
     'opts': ['A delivery van a bakery uses for its orders',
              "The savings balance in a bakery's bank account",
              'An untouched deposit of iron ore in the ground',
              'The hours a baker spends shaping loaves of bread'],
     'exp': 'In economics, capital means human-made resources used to produce goods and services, such '
            "as machines, tools, buildings, and vehicles. The bakery's delivery van is a human-made "
            'resource used in production.',
     'why': [None,
             'Everyday speech calls money capital, but a bank balance is not itself a productive '
             'resource. Economists reserve the term for human-made resources like equipment.',
             'Iron ore in the ground is a natural resource provided by nature, not a human-made '
             "resource, so it isn't capital.",
             "A baker's working hours are labor, a human resource, not capital. Capital refers to the "
             'human-made tools and equipment that labor works with.']},
    # id 81
    {'ch': 1,
     'q': 'Economists use the term rationing to mean:',
     'opts': ['Allocating a limited supply among people who want more of it',
              'Government coupon programs used during wartime shortages',
              "Producing more of a good until everyone's wants are met",
              'Holding prices low so that every buyer can afford the good'],
     'exp': 'Rationing is the allocation of a limited supply of a good or resource among people who '
            'want more of it. Because of scarcity, every society must ration somehow, whether by '
            'price, first-come, first-served, or another method.',
     'why': [None,
             'Coupon programs are one rationing method, but the economic term is broader: allocating '
             'by price or by first-come, first-served is rationing too.',
             "Producing until all wants are met isn't possible under scarcity. Rationing is needed "
             'precisely because wants exceed the available supply.',
             "Holding prices low doesn't remove the need to ration; it just shifts allocation to "
             'another method, such as waiting in line.']},
    # id 82 (retired)
    {'ch': 1,
     'q': 'When price is used to ration goods, people have a strong incentive to:',
     'opts': ['Earn income so they can pay the required price',
              'Wait in long lines',
              'Avoid working',
              'Lobby the government for coupons'],
     'exp': 'Price rationing allocates goods to those willing to give up other things. That rewards '
            'earning income, which in turn encourages productive activity.',
     'retired': True},
    # id 83 (retired)
    {'ch': 1,
     'q': 'How many guideposts (key principles) of the economic way of thinking does Gwartney '
          'identify?',
     'opts': ['Eight', 'Five', 'Ten', 'Twelve'],
     'exp': 'Chapter 1 lists eight guideposts: trade-offs, purposeful choice, incentives, marginal '
            'decisions, costly information, secondary effects, subjective value, and testing theories '
            'by prediction.',
     'retired': True},
    # id 84 (retired)
    {'ch': 1,
     'q': 'A parcel of land could become a hospital, a parking lot, or stay undeveloped. Guidepost 1 '
          'says:',
     'opts': ['No option is free; choosing one means a trade-off',
              'Leaving it undeveloped costs nothing',
              'The hospital is always the best choice',
              'Government should decide its use'],
     'exp': 'Guidepost 1: the use of scarce resources is costly, so decision-makers face trade-offs. '
            "Even 'leaving it alone' gives up the next best use.",
     'retired': True},
    # id 85 (retired)
    {'ch': 1,
     'q': 'Pizza, lobster, and steak would give you identical benefits, so you pick the pizza because '
          "it's cheapest. This illustrates:",
     'opts': ['Economizing behavior (individuals choose purposefully)',
              'The fallacy of composition',
              'Secondary effects',
              'Value is objective'],
     'exp': 'Guidepost 2: people choose purposefully, trying to get the most from limited resources. '
            'With equal benefits, they choose the lowest-cost option.',
     'retired': True},
    # id 86 (retired)
    {'ch': 1,
     'q': 'A store owner cuts prices to sell off excess inventory, expecting more customers to buy. '
          'Which guidepost explains this?',
     'opts': ['Incentives matter',
              'Information is costly',
              'Value is subjective',
              'Association is not causation'],
     'exp': 'Guidepost 3: changes in incentives influence choices in predictable ways. A lower price '
            'is an incentive to buy more.',
     'retired': True},
    # id 87 (retired)
    {'ch': 1,
     'q': 'According to Guidepost 3, which incentives influence human choices?',
     'opts': ['Both monetary and nonmonetary incentives',
              'Only monetary incentives',
              'Only nonmonetary incentives',
              'Only incentives created by government'],
     'exp': 'Incentives matter whether they involve money (prices, wages) or not (time, praise, '
            'safety, convenience).',
     'retired': True},
    # id 88
    {'ch': 1,
     'q': 'An economist says a firm should decide **at the margin**. This means the firm should focus '
          'on:',
     'opts': ['The added benefit and added cost of a change from where it is now',
              'The total benefit and total cost of everything it has produced',
              'The average cost per unit across the output it has made so far',
              'The fixed costs it must pay no matter how much it produces'],
     'exp': 'Marginal describes the effects of a change in the current situation, such as the added '
            'cost of one more unit given current facilities and output. Deciding at the margin means '
            'weighing the added benefit against the added cost.',
     'why': [None,
             "Totals include past choices the decision can't change. Marginal thinking looks only at "
             'the extra benefit and extra cost of the change being considered.',
             'Average cost mixes in units already made. The relevant cost of a change is the added '
             'cost of that change, not an average over past output.',
             "Fixed costs don't change with the decision, so they don't matter at the margin. Marginal "
             'analysis focuses on the costs the change adds.']},
    # id 89 (retired)
    {'ch': 1,
     'q': "A producer's marginal cost is:",
     'opts': ['The cost of producing one additional unit, given its current facility and output',
              'Total cost divided by the number of units',
              'The cost of building a new factory',
              'The fixed cost the firm pays regardless of output'],
     'exp': 'Marginal cost is the change in cost from producing one more unit, starting from the '
            'current production rate.',
     'retired': True},
    # id 90 (retired)
    {'ch': 1,
     'q': 'You compare jeans at a few stores, then stop shopping and buy with the information you '
          'have. This reflects which guidepost?',
     'opts': ['Acquiring information is costly',
              'Incentives matter',
              'Value is subjective',
              'The test of a theory is its ability to predict'],
     'exp': 'Guidepost 5: information helps us choose, but gathering it takes scarce time. At some '
            "point more comparison-shopping isn't worth the trouble.",
     'retired': True},
    # id 91 (retired)
    {'ch': 1,
     'q': 'San Francisco banned plastic grocery bags to help the environment, but reusable bags can '
          'gather harmful bacteria. This is an example of:',
     'opts': ['A secondary effect',
              'Economizing behavior',
              'A marginal decision',
              'Positive economics'],
     'exp': "Guidepost 6: economic actions often have indirect effects that aren't immediately "
            'observable, in addition to their direct effects.',
     'retired': True},
    # id 92 (retired)
    {'ch': 1,
     'q': 'In public policy, secondary effects are often:',
     'opts': ['Unintended and overlooked',
              'The main reason a policy is passed',
              'Easy to observe immediately',
              'Always beneficial'],
     'exp': 'Secondary effects are indirect impacts that may not be easily or immediately seen, so '
            'policymakers frequently miss them.',
     'retired': True},
    # id 93 (retired)
    {'ch': 1,
     'q': 'Amir prefers a grass field next to work; Camilla prefers a parking lot and a shorter walk. '
          'This illustrates:',
     'opts': ['Value is subjective and varies with individual preferences',
              'Association is not causation',
              'Ceteris paribus',
              "Incentives don't matter"],
     'exp': "Guidepost 7: the value of a good depends on each person's preferences, so the same field "
            'is worth different amounts to different people.',
     'retired': True},
    # id 94 (retired)
    {'ch': 1,
     'q': "'The earth is made of marshmallows' is classified as:",
     'opts': ["A positive statement, because it is potentially verifiable (even though it's false)",
              'A normative statement, because it is false',
              'A normative statement, because it is about the earth',
              'Neither positive nor normative'],
     'exp': "Positive statements are about 'what is' and can be tested. They don't have to be correct. "
            "Normative statements are about 'what ought to be'.",
     'retired': True},
    # id 95 (retired)
    {'ch': 1,
     'q': 'A politician backs a well-meaning policy that ends up causing harm. Which pitfall does this '
          'illustrate?',
     'opts': ['Good intentions do not guarantee desirable outcomes',
              'The fallacy of composition',
              'Association is not causation',
              'Violation of ceteris paribus'],
     'exp': 'An unsound proposal leads to bad outcomes even when supporters mean well. Politicians may '
            'gain from appearing to address a problem even if the policy is ineffective.',
     'retired': True},
    # id 96 (retired)
    {'ch': 1,
     'q': 'Cities with more police officers tend to have more crime, so someone concludes police cause '
          'crime. This mistake is:',
     'opts': ['Assuming association is causation',
              'The fallacy of composition',
              'Normative reasoning',
              'Economizing behavior'],
     'exp': 'Pitfall 3: statistical association alone cannot establish causation. Here, high crime '
            'more likely causes cities to hire more police.',
     'retired': True},
    # id 97
    {'ch': 1,
     'q': 'Which of these is a macroeconomic question?',
     'opts': ["Why did the nation's overall unemployment rate rise last year?",
              "How will a coffee shop's price increase affect its own sales?",
              'How does a single family decide how much of its income to save?',
              'Why did one automaker decide to close one of its older plants?'],
     'exp': 'Macroeconomics studies outcomes in highly aggregated markets, such as the economy-wide '
            "labor market. A nation's overall unemployment rate is an economy-wide outcome.",
     'why': [None,
             "One coffee shop's pricing and sales concern a single firm, a narrowly defined unit, "
             'which makes this a microeconomic question.',
             "A single household's saving choice concerns one narrowly defined unit, so it is "
             'microeconomics, even though saving also matters for the economy as a whole.',
             "One automaker's plant decision involves a single business firm, so it is microeconomics, "
             'however large the firm is.']},
    # id 98
    {'ch': 2,
     'q': 'Two students skip the same Friday party to study. Which statement about their opportunity '
          'costs is correct?',
     'opts': ['Their costs can differ, since each values the forgone party differently',
              'Their costs must be equal, since they gave up the very same event',
              'Their costs are zero, because the party had no admission charge',
              'Their costs are measured by the grades they earn from studying'],
     'exp': 'Opportunity costs are subjective and vary across persons. Each student values the forgone '
            'party differently, so skipping the same event can cost them different amounts.',
     'why': [None,
             "Giving up the same event doesn't mean the same cost. The cost depends on how much each "
             'person values what was given up.',
             'A free party still has an opportunity cost: the value each student places on attending. '
             "Opportunity cost isn't limited to money charges.",
             'Grades are the benefit of studying, not its cost. The cost is the value of the party '
             'each student gave up.']},
    # id 99 (retired)
    {'ch': 2,
     'q': 'If an option becomes more costly, an individual will be:',
     'opts': ['Less likely to choose it',
              'More likely to choose it',
              'Unaffected, since costs are already sunk',
              'Forced to choose it'],
     'exp': 'Raising the opportunity cost of an option makes it less attractive relative to the '
            'alternatives.',
     'retired': True},
    # id 100
    {'ch': 2,
     'q': 'Gwartney splits the opportunity cost of attending college into monetary and non-monetary '
          'parts. Which is classified as non-monetary?',
     'opts': ['The earnings from a job you give up to attend',
              'The tuition you pay to the college each term',
              'The price of required textbooks and software',
              'The fees charged for labs and student services'],
     'exp': 'Gwartney lists tuition and books as monetary costs and forgone earnings as the '
            "non-monetary cost of college. You don't pay forgone earnings out of pocket; you give them "
            'up by not working.',
     'why': [None,
             'Tuition is a direct money payment, which Gwartney classifies as a monetary cost of '
             'college.',
             'Textbooks and software are bought with money, so they fall under monetary costs, like '
             "the books in Gwartney's example.",
             'Lab and service fees are money payments to the college, so they are monetary costs, just '
             'like tuition.']},
    # id 101 (retired)
    {'ch': 2,
     'q': 'You get a fantastic job offer right out of high school. Your opportunity cost of attending '
          'college:',
     'opts': ["Rises, so you're less likely to attend",
              "Falls, so you're more likely to attend",
              "Stays the same, since tuition didn't change",
              'Becomes zero'],
     'exp': "The great job is the alternative you'd give up. A more valuable alternative means a "
            'higher opportunity cost of college.',
     'retired': True},
    # id 102 (retired)
    {'ch': 2,
     'q': 'According to Gwartney, the value of a good or service:',
     'opts': ["Depends on who uses it and the circumstances of when and where it's used",
              'Is fixed and objective once the good exists',
              'Is determined only by its production cost',
              'Is set by the government'],
     'exp': "It's wrong to assume goods have a fixed objective value. Value depends on the user, "
            'timing, location, and physical traits.',
     'retired': True},
    # id 103 (retired)
    {'ch': 2,
     'q': 'Even when no additional goods are produced, trade creates value by:',
     'opts': ['Moving goods from people who value them less to people who value them more',
              'Ensuring each good is exchanged for one of equal objective value',
              'Raising prices for everyone',
              "Making one party better off at the other's expense"],
     'exp': 'Even without producing anything new, trade channels goods to those who value them most, '
            "increasing the wealth created by society's resources.",
     'retired': True},
    # id 104 (retired)
    {'ch': 2,
     'q': 'Milton and Rose Friedman argued that most economic fallacies come from neglecting the fact '
          'that:',
     'opts': ["A voluntary exchange won't take place unless both parties believe they'll benefit",
              'Prices always rise over time',
              'Trade is a zero-sum game',
              'Governments must approve all trades'],
     'exp': "Mutual gain is the foundation of trade. If both sides didn't expect to gain, the "
            "voluntary exchange wouldn't happen.",
     'retired': True},
    # id 105
    {'ch': 2,
     'q': 'Which of these is an example of a transaction cost?',
     'opts': ['Hours spent searching listings and haggling to buy a used car',
              'The wages a car factory pays its workers on the assembly line',
              'The steel and glass used in manufacturing a brand-new car',
              'The value of a car to its buyer minus the price that was paid'],
     'exp': 'Transaction costs are the time, effort, and other resources needed to search out, '
            'negotiate, and complete an exchange. Hours spent searching listings and haggling are '
            'costs of making the trade itself.',
     'why': [None,
             'Assembly-line wages are a cost of producing the car, not of arranging its sale. '
             'Transaction costs come from completing an exchange.',
             'Steel and glass are production inputs. Transaction costs are the time and effort needed '
             'to arrange and complete a trade.',
             "Value minus price is the buyer's gain from the trade, not a cost. Transaction costs "
             'reduce that gain rather than measure it.']},
    # id 106 (retired)
    {'ch': 2,
     'q': 'How does the Internet affect trade?',
     'opts': ['It lowers transaction costs, enhancing trade',
              'It raises transaction costs, reducing trade',
              'It has no effect on transaction costs',
              'It eliminates the need for property rights'],
     'exp': 'Online search, reviews, and payment systems make it cheaper to find, negotiate, and '
            'complete exchanges, so more mutually beneficial trades happen.',
     'retired': True},
    # id 107 (retired)
    {'ch': 2,
     'q': 'Property rights are defined as:',
     'opts': ['The right to use, control, and obtain the benefits from a resource, good, or service',
              'The right to have the government buy your property',
              "The right to use anyone's property freely",
              'The right to set any price the market will not bear'],
     'exp': 'Private property rights involve exclusive use, legal protection against invaders, and the '
            'right to transfer to another.',
     'retired': True},
    # id 108 (retired)
    {'ch': 2,
     'q': 'Why do private owners tend to conserve resources for the future?',
     'opts': ['They gain if the property is expected to increase in value',
              'The law requires them to',
              "They don't bear any costs of using it up",
              'Government pays them to'],
     'exp': 'Private owners capture the future value of what they own, so conserving it pays off, '
            "especially when it's expected to appreciate.",
     'retired': True},
    # id 109 (retired)
    {'ch': 2,
     'q': 'Private property encourages owners to use resources in ways that benefit others because '
          'owners:',
     'opts': ["Gain by serving others and bear the opportunity cost of ignoring others' wishes",
              'Are required to share profits with neighbors',
              "Can't sell their property",
              'Receive government subsidies for doing so'],
     'exp': 'If an owner ignores what others value, they lose the income those others would have paid. '
            'That cost pushes owners toward uses others value.',
     'retired': True},
    # id 110
    {'ch': 2,
     'q': 'Which is **not** an assumption used in drawing a production possibilities curve (PPC)?',
     'opts': ['Resources expand during the period',
              'The amount of resources is fixed',
              'Technical knowledge is held given',
              'Resources are fully and efficiently used'],
     'exp': 'A PPC shows all output combinations possible with a fixed amount of resources, a given '
            'level of technical knowledge, and full, efficient use of those resources. If resources '
            'expanded, the whole curve would shift outward instead of staying put.',
     'why': [None,
             'A fixed amount of resources is one of the three PPC assumptions; it is what makes the '
             'curve a limit on output.',
             'Given technical knowledge is a PPC assumption. Better technology would shift the curve, '
             'so it is held constant to draw a single curve.',
             'Full and efficient use of resources is a PPC assumption; it is why points on the curve '
             'are efficient and points inside are not.'],
     'fig': {'type': 'graph',
             'x': 'Clothing',
             'y': 'Food',
             'lines': [{'pts': [[8, 70], [25, 66], [40, 58], [52, 45], [60, 28], [64, 8]],
                        'cls': 's',
                        'label': 'PPC'}],
             'guides': False,
             'alt': 'A bowed-out production possibilities curve, labeled PPC, with food on the '
                    'vertical axis and clothing on the horizontal axis.'},
     'expFig': {'type': 'graph',
                'x': 'Clothing',
                'y': 'Food',
                'lines': [{'pts': [[8, 70], [25, 66], [40, 58], [52, 45], [60, 28], [64, 8]],
                           'cls': 'm',
                           'label': 'PPC1'},
                          {'pts': [[8, 88], [30, 84], [50, 74], [66, 58], [78, 38], [85, 8]],
                           'cls': 's',
                           'label': 'PPC2',
                           'dash': True}],
                'arrows': [{'from': [44, 54], 'to': [56, 66]}],
                'guides': False,
                'alt': 'Two bowed-out production possibilities curves for food and clothing. PPC1 is '
                       'closer to the origin; PPC2 lies farther out. An arrow points from PPC1 toward '
                       'PPC2, showing the whole curve moving outward when resources expand.'}},
    # id 111 (retired)
    {'ch': 2,
     'q': 'The slope of the production possibilities curve shows:',
     'opts': ['How much of one good must be given up to produce more of the other',
              'The total value of all output',
              'The price of each good',
              'How much labor is unemployed'],
     'exp': 'The slope is the opportunity cost of producing more of one product, measured in units of '
            'the other.',
     'retired': True},
    # id 112 (retired)
    {'ch': 2,
     'q': 'With 10 hours of study, Susan can get a B in English and a B in economics, or an A in '
          'English and a D in economics. Her opportunity cost of raising English from B to A is:',
     'opts': ['Her economics grade falling from B to D',
              'Nothing, since study time is free',
              'Her English grade falling from A to B',
              'Studying more than 10 hours'],
     'exp': 'Moving along her PPC from T to U, she gains in English only by shifting hours away from '
            'economics. The lost economics grade is the opportunity cost.',
     'retired': True},
    # id 113 (retired)
    {'ch': 2,
     'q': "Which of these could shift a country's PPC outward?",
     'opts': ['An improvement in the rules under which the economy functions',
              'Moving workers from farming to manufacturing',
              'Leaving some factories idle',
              'Higher prices for consumer goods'],
     'exp': 'The four outward shifters are: more resources, better technology, improved rules '
            '(institutions), and working harder by giving up leisure.',
     'retired': True},
    # id 114
    {'ch': 2,
     'q': 'Which best describes an entrepreneur?',
     'opts': ['Someone who decides what resources to use, how to combine them, and what to make',
              'Someone who lends money to businesses in return for regular interest payments',
              "Someone who buys and resells goods to cut other people's costs of trading",
              "Someone hired by a firm's owners to run its day-to-day operations for a salary"],
     'exp': 'An entrepreneur decides what resources will be used, how they will be combined, and what '
            'goods and services they will produce. Entrepreneurs who produce highly valued goods can '
            "expand the economy's production possibilities.",
     'why': [None,
             'Lending money for interest describes a lender. The entrepreneur is the one deciding how '
             'to combine resources and what to produce.',
             'Buying and reselling to cut trading costs describes a middleman, a different role in '
             'this chapter.',
             "A salaried manager runs operations on the owners' behalf. The entrepreneur is the one "
             'deciding which resources to combine and what to make.']},
    # id 115
    {'ch': 2,
     'q': 'Within the production possibilities framework, economic growth appears as:',
     'opts': ['The curve itself shifting outward as time passes',
              'A move from a point inside the curve onto the curve',
              'A move along the curve toward more capital goods',
              'A steeper slope at each point on the existing curve'],
     'exp': 'In the PPC framework, economic growth is an outward shift of the curve through time; the '
            'faster it shifts, the faster the growth. More of all goods becomes possible.',
     'why': [None,
             "Moving from inside the curve onto it uses existing resources more fully, but it doesn't "
             'expand what is possible. Only an outward shift is growth.',
             'Moving along the curve changes the mix of goods made with current resources. More '
             "capital goods may bring future growth, but the move itself isn't growth.",
             'A steeper slope changes the trade-off between the goods, not how much can be produced '
             'overall. Growth means the curve moves outward.']},
    # id 116 (retired)
    {'ch': 5,
     'q': 'Economists use efficiency to judge actions because efficient use of resources implies:',
     'opts': ['The maximum value of output from the resource base',
              'The lowest possible prices',
              'Equal incomes for everyone',
              'Zero pollution'],
     'exp': 'Efficiency means getting the most value from limited resources: undertaking actions whose '
            'benefits exceed costs and avoiding those whose costs exceed benefits.',
     'retired': True},
    # id 117 (retired)
    {'ch': 5,
     'q': 'At an output level where marginal benefit EXCEEDS marginal cost, the activity should be:',
     'opts': ["Expanded, because worthwhile units aren't being undertaken",
              'Reduced, because too much is being produced',
              "Left unchanged, because it's efficient",
              'Stopped entirely'],
     'exp': 'If MB > MC, the next unit adds more value than it costs. Expanding until MB = MC captures '
            'those gains.',
     'retired': True},
    # id 118 (retired)
    {'ch': 5,
     'q': 'At an output level where marginal cost EXCEEDS marginal benefit:',
     'opts': ["Units are being produced that cost more than they're worth, so output is too high",
              'Output is too low',
              'The activity is efficient',
              'Marginal benefit must rise'],
     'exp': 'Producing units where MC > MB wastes resources. Efficiency requires cutting back to where '
            'MB = MC.',
     'retired': True},
    # id 119
    {'ch': 5,
     'q': '"If it\'s worth doing, it\'s worth doing imperfectly." In economic terms this means:',
     'opts': ['Beyond some point, the gain from doing a task better is less than the cost',
              'Tasks worth doing should be done as cheaply as possible, whatever the result',
              'Government programs should stop short of perfection, but personal choices need not',
              'A worthy goal justifies any cost once its total benefit exceeds its total cost'],
     'exp': 'At some point the extra gain from doing something better is not worth the extra cost, so '
            'it makes sense to stop short of perfection. Economics is about trade-offs, even for '
            'worthy activities.',
     'why': [None,
             'The principle does not say to minimize cost regardless of results. It says to keep '
             'improving while the added benefit exceeds the added cost, then stop.',
             'The text says the principle applies regardless of sector: perfection is generally not '
             'worth the cost in personal and government decisions alike.',
             'Comparing totals misses the margin. Even when total benefit exceeds total cost, units '
             'beyond the efficient level add more cost than benefit, so not every cost is justified.']},
    # id 120 (retired)
    {'ch': 5,
     'q': 'From an efficiency standpoint, eliminating ALL air and water pollution:',
     'opts': ["Generally doesn't make sense, because the cost of removing the last bits would exceed "
              'the benefit',
              'Always makes sense, because pollution is harmful',
              'Is required for efficiency',
              'Has no cost'],
     'exp': 'Like making the highest possible grade or zero traffic fatalities, perfection is rarely '
            'worth its cost. The efficient level is where MB = MC.',
     'retired': True},
    # id 121
    {'ch': 5,
     'q': "In the text's framework, providing a stable monetary and financial environment belongs with "
          'which government role?',
     'opts': ['Productive function, alongside goods hard to supply through markets',
              'Protective function, alongside enforcing contracts and property rights',
              'Protective function, alongside defense against acts of aggression',
              'Neither function; it is left to private banks and markets to supply'],
     'exp': 'The chapter lists a stable monetary and financial environment under the productive '
            'function, which provides a limited set of goods that are difficult to supply through the '
            'market.',
     'why': [None,
             'The protective function is about guarding people and property and enforcing contracts. '
             'Monetary stability supports markets, but this chapter places it with the goods '
             'government produces.',
             "Defense against aggression is protective, but a stable money supply isn't about guarding "
             'against invasion. The chapter lists it as something government provides, under the '
             'productive function.',
             'The chapter calls a stable monetary and financial environment vital and lists it among '
             'the goods government provides, so it is not left to private banks alone.']},
    # id 122 (retired)
    {'ch': 5,
     'q': 'The most fundamental function of government is:',
     'opts': ['Protecting individuals and their property against acts of aggression',
              'Producing consumer goods',
              'Setting prices in markets',
              'Redistributing income'],
     'exp': 'The protective function includes maintaining a legal structure that enforces contracts '
            'and settles disputes.',
     'retired': True},
    # id 123 (retired)
    {'ch': 5,
     'q': 'If producers can restrict supply or limit entry into a market, compared to the competitive '
          'outcome:',
     'opts': ['Output will be lower and price will be higher',
              'Output will be higher and price will be lower',
              'Output and price will both be higher',
              'Nothing changes'],
     'exp': 'With restricted supply (S2), output falls from Q1 to Q2 and price rises from P1 to P2: '
            'too few units at too high a price.',
     'retired': True},
    # id 124
    {'ch': 5,
     'q': 'External costs such as pollution arise mainly because:',
     'opts': ['Property rights are poorly defined or weakly enforced',
              'Producers charge prices well above the competitive level',
              'Consumers lack information about product quality',
              'Goods are nonrival in consumption and nonexcludable'],
     'exp': "External costs arise when actions harm others' property without their consent. That "
            "happens because property rights are imperfectly defined or enforced, so polluters don't "
            'pay for the damage they do.',
     'why': [None,
             'Prices above the competitive level come from a lack of competition, a separate source of '
             'market failure. Pollution can occur even in highly competitive industries.',
             "Poor information concerns buyers who can't judge what they are buying. Pollution harms "
             'people outside the transaction, who never agreed to bear the cost.',
             'Nonrival and nonexcludable describe public goods, a different market failure. External '
             "costs stem from property rights that aren't well defined or enforced."]},
    # id 125 (retired)
    {'ch': 5,
     'q': 'When external costs are present, the market supply curve:',
     'opts': ['Understates the true cost of production',
              'Overstates the true cost of production',
              'Accurately reflects all costs',
              'Becomes vertical'],
     'exp': "Since some costs fall on others, producers don't count them. Units get produced that are "
            'worth less than their full cost.',
     'retired': True},
    # id 126 (retired)
    {'ch': 5,
     'q': "When it isn't realistic to define property rights (many people are affected), what may be "
          'the best way to handle external costs such as emissions?',
     'opts': ['Government regulations requiring devices that limit emissions',
              'Doing nothing, since markets always correct themselves',
              'Banning all production',
              'Subsidizing the polluting firms'],
     'exp': 'Defining and enforcing property rights works with few parties. With large numbers, '
            'emission-limiting regulations, or creative arrangements, may be the best option.',
     'retired': True},
    # id 127
    {'ch': 5,
     'q': 'When an activity creates external benefits, the market demand curve:',
     'opts': ['Understates the total value of the output',
              'Overstates the total value of the output',
              'Understates the true cost of the output',
              'Shifts right on its own to reflect outside benefits'],
     'exp': 'With external benefits, part of the value goes to people who are not buyers. Market '
            "demand reflects only buyers' own benefits, so it understates the output's total value and "
            'too few units are often produced.',
     'why': [None,
             'This reverses the direction. Buyers ignore the benefits that go to nonparticipants, so '
             'demand reflects less value than the output actually provides, not more.',
             'That is the problem with external costs, and it concerns the supply curve. External '
             'benefits are about value, so it is the demand curve that falls short.',
             'The market does not register external benefits on its own. Demand would include them '
             'only if all benefits were counted, and buyers weigh just their own benefits.'],
     'expFig': {'type': 'graph',
                'x': 'Quantity',
                'y': 'Price',
                'lines': [{'pts': [[10, 15], [90, 85]], 'cls': 's', 'label': 'S'},
                          {'pts': [[10, 71], [78, 11.5]], 'cls': 'd', 'label': 'D1'},
                          {'pts': [[10, 92], [90, 22]], 'cls': 'd', 'label': 'D2', 'dash': True}],
                'points': [{'at': [42, 43], 'label': 'E1'}, {'at': [54, 53.5], 'label': 'E2'}],
                'guides': True,
                'xticks': [[42, 'Q1'], [54, 'Q2']],
                'yticks': [[43, 'P1'], [53.5, 'P2']],
                'alt': 'An upward-sloping supply curve S crosses the market demand curve D1 at E1, at '
                       'quantity Q1 and price P1. A dashed demand curve D2, showing demand if all '
                       'benefits were counted, lies to the right of D1 and crosses S at E2, at the '
                       'larger quantity Q2 and the higher price P2. The market itself settles at E1.'}},
    # id 128 (retired)
    {'ch': 5,
     'q': 'If all external benefits were counted, the demand curve would shift to D2. Compared with '
          'the market outcome, output and price would be:',
     'opts': ['Output higher and price higher',
              'Output lower and price lower',
              'Output higher and price lower',
              'Unchanged'],
     'exp': 'Counting all benefits raises demand, so output rises from Q1 to Q2 and price rises from '
            'P1 to P2. The market alone produces too few units.',
     'retired': True},
    # id 129 (retired)
    {'ch': 5,
     'q': 'Which of these is an example of a public good?',
     'opts': ['A mosquito abatement program', 'A pizza', 'A haircut', 'A new car'],
     'exp': 'Mosquito control is nonrival and nonexcludable: everyone in the area benefits at once, '
            "and nonpayers can't be excluded. National defense and broadcast signals are other "
            'examples.',
     'retired': True},
    # id 130 (retired)
    {'ch': 5,
     'q': 'What distinguishes a good as a public good?',
     'opts': ['Its characteristics (nonrival and nonexcludable), not the sector that produces it',
              'Whether government produces it',
              "Whether it's free",
              "Whether it's sold in a market"],
     'exp': "Government can provide private goods and markets can provide public goods. The good's "
            'traits define it.',
     'retired': True},
    # id 131
    {'ch': 5,
     'q': "A consumer's information problem is smallest when the item is:",
     'opts': ['Bought often by the same buyer from the same seller',
              'Expensive and purchased once or twice in a lifetime',
              'Hard to judge even after a careful inspection',
              'Capable of harm that a layperson cannot predict'],
     'exp': 'When an item is bought often by the same buyer, the buyer learns from experience and the '
            'seller wants the repeat business, so the information problem is minimal.',
     'why': [None,
             'Items bought once or twice give buyers no chance to learn from experience and give '
             'sellers little reason to protect repeat business, so information problems are larger.',
             'Goods that are difficult to evaluate even after inspection are exactly where the text '
             'says conflicts and unhappy customers arise.',
             "Serious harm that a layperson can't predict is one of the text's conditions for an "
             'information problem, so this case makes the problem worse, not smaller.']},
    # id 132 (retired)
    {'ch': 5,
     'q': 'Consumer Reports, brand names, franchises, and online reviews show that:',
     'opts': ['Information can be a profit opportunity, since consumers will pay for better '
              'information',
              'Markets can never solve information problems',
              'Government must provide all product information',
              'Information is free'],
     'exp': 'Because consumers value better information, businesses profit by providing expert '
            'evaluations and reliable standardized quality.',
     'retired': True},
    # id 133 (retired)
    {'ch': 6,
     'q': 'Transfer payments are:',
     'opts': ['Payments that tax income from some people and transfer it to others',
              'Payments for government purchases of goods',
              'Interest paid on government bonds',
              'Wages paid to government employees'],
     'exp': 'Transfer payments (like Social Security) redistribute income rather than buying output, '
            'and they have grown substantially over time.',
     'retired': True},
    # id 134
    {'ch': 6,
     'q': 'Which is a similarity between the government and market sectors?',
     'opts': ['Both face scarcity, and competition is present in both',
              'Both base decisions on mutual agreement among parties',
              "Both tie each person's payment to what they consume",
              'Both give the most influence to those with high income'],
     'exp': 'Competition and scarcity exist in both sectors. Resources government uses are unavailable '
            'for other goods, even if the output is provided free to users.',
     'why': [None,
             'Mutual agreement describes markets. Democratic government acts by majority rule, which '
             'can bind people who voted no.',
             'Payment matches consumption in markets, but government can disconnect what each person '
             'pays from the benefits they receive.',
             'Income drives purchasing power in markets. In politics, influence goes to those most '
             'willing to contribute time, organization, persuasion, and money.']},
    # id 135 (retired)
    {'ch': 6,
     'q': 'Voters must choose candidates who represent a whole bundle of positions. This '
          "'bundle-purchase' problem:",
     'opts': ["Limits individual voters' power to make their preferences count on specific issues",
              'Is common in markets',
              'Gives voters more choice than markets do',
              'Only affects politicians'],
     'exp': "In markets you can buy exactly the items you want. In politics you get a candidate's "
            'entire package, so specific preferences are hard to express.',
     'retired': True},
    # id 136
    {'ch': 6,
     'q': 'Private-sector action rests on ___, while democratic public-sector action rests on ___.',
     'opts': ['mutual agreement; majority rule',
              'majority rule; mutual agreement',
              'competition; the absence of competition',
              "consumer income; bureaucrats' choices"],
     'exp': 'Market exchanges happen only when both parties agree, while democratic government acts by '
            'majority rule, which can bind people who voted against the action.',
     'why': [None,
             "This swaps the two. Markets require each party's consent; it is democratic government "
             'that decides by majority.',
             "Competition is present in both sectors, so it can't be what separates them; politicians "
             'compete for votes much as firms compete for customers.',
             "Income shapes how much people can buy, but it isn't the basis of private action, and "
             "democratic action rests on majority rule rather than bureaucrats' choices."]},
    # id 137 (retired)
    {'ch': 6,
     'q': 'In the political sector, who tends to have the most influence?',
     'opts': ['Those most able and willing to use their time, persuasion, organization, and '
              'contributions to help politicians get votes',
              'Those with the highest incomes, exactly as in markets',
              'Every voter equally',
              'Bureaucrats only'],
     'exp': 'Influence is distributed differently than in markets: political activity and support, not '
            'just income, buy political influence.',
     'retired': True},
    # id 138
    {'ch': 6,
     'q': 'Public choice analysis treats the political process as an interaction among:',
     'opts': ['Voter-taxpayers, politicians, and bureaucrats',
              'Consumers, business producers, and resource owners',
              'Voters, the courts, and the central bank',
              'Politicians, lobbyists, and news media'],
     'exp': 'Public choice applies the tools of economics to politics, viewing it as an interaction '
            'among voter-taxpayers, politicians, and bureaucrats, each acting in their own interest.',
     'why': [None,
             'These are the participants in the market sector. Public choice models the political '
             "sector's own players instead.",
             "Courts and the central bank aren't among the three groups in the public choice "
             'framework, which pairs voters with politicians and bureaucrats.',
             "Lobbyists matter through the special interest effect, but the framework's three groups "
             'are voter-taxpayers, politicians, and bureaucrats, not lobbyists and media.']},
    # id 139 (retired)
    {'ch': 6,
     'q': 'According to public choice analysis, the primary motivation of politicians is:',
     'opts': ['Winning elections',
              'Maximizing economic efficiency',
              'Reducing the size of government',
              'Maximizing profits'],
     'exp': 'Votes are the lifeblood of the politician, just as profits are for the market '
            'entrepreneur.',
     'retired': True},
    # id 140
    {'ch': 6,
     'q': 'According to public choice analysis, government bureaucrats are generally better off with:',
     'opts': ['Larger budgets and expanded programs',
              'Lower costs so funds return to taxpayers',
              'Smaller agencies that are easier to run',
              'Programs ended once their goals are met'],
     'exp': 'Bureaucrats seek promotions, job security, and power, and larger budgets and expanded '
            'programs generally serve those goals.',
     'why': [None,
             'Public-sector managers seldom gain personally from cutting costs, so returning savings '
             'to taxpayers does little for their own interests.',
             'Smaller agencies mean fewer promotions and less power, which runs against the goals '
             'public choice assigns to bureaucrats.',
             "Ending a program shrinks budgets and jobs. Bureaucrats' interests favor keeping and "
             'expanding programs, even after the original goals are met.']},
    # id 141 (retired)
    {'ch': 6,
     'q': 'Road project: Plan B makes each voter pay in proportion to the benefits they receive. What '
          'happens in the vote?',
     'opts': ['It passes unanimously, since every voter gains',
              'It fails 3 to 2',
              'It passes 3 to 2',
              'It fails unanimously'],
     'exp': 'When costs are allocated in proportion to benefits, everyone gains from a productive '
            "project. That's when good politics and efficiency are in harmony.",
     'retired': True},
    # id 142 (retired)
    {'ch': 6,
     'q': "When a project's benefits are widespread but its costs are concentrated, the political "
          'process tends to:',
     'opts': ["Reject projects even when they're productive",
              "Adopt projects even when they're counterproductive",
              'Make efficient decisions',
              'Have no bias'],
     'exp': "This is type 4. The few who bear concentrated costs fight hard, while the many who'd gain "
            'a little pay little attention.',
     'retired': True},
    # id 143 (retired)
    {'ch': 6,
     'q': 'When benefits and costs are BOTH widespread (or both concentrated), representative '
          'government tends to:',
     'opts': ['Undertake productive projects and reject unproductive ones',
              'Adopt inefficient projects',
              'Reject all projects',
              'Ignore the projects'],
     'exp': 'Types 1 and 3 work reasonably well: the people who gain and the people who pay weigh in '
            'similarly, so politics tracks efficiency.',
     'retired': True},
    # id 144 (retired)
    {'ch': 6,
     'q': 'A bill combines a post office in district A, a harbor in B, and a stadium in C. Each '
          "project nets its own district +$10 but costs every other district $3, so the bill's total "
          'is -$6. How can it still pass?',
     'opts': ['Representatives of A, B, and C trade votes (logrolling) to form a majority',
              'Districts D and E vote for it',
              "It can't pass, since the total is negative",
              'The president passes it without a vote'],
     'exp': 'Vote trading lets a majority pass a package of projects that each benefit a few '
            'districts, even though the whole package is counterproductive.',
     'retired': True},
    # id 145 (retired)
    {'ch': 6,
     'q': 'Politicians often favor established firms (like taxi companies over Uber) because '
          'established firms:',
     'opts': ['Have stronger records of political contributions and know lobbying techniques',
              'Are always more efficient',
              'Pay lower taxes',
              'Have more customers'],
     'exp': 'Logrolling and pork-barrel politics strengthen the special interest effect, favoring '
            'politically connected incumbents over innovative upstarts.',
     'retired': True},
    # id 146 (retired)
    {'ch': 6,
     'q': 'What is the effect of widespread rent seeking on an economy?',
     'opts': ['It diverts resources away from productive activities, so output falls below potential',
              'It increases output above potential',
              'It has no effect on output',
              'It improves the efficiency of government'],
     'exp': "Resources spent lobbying for favors aren't spent producing goods. The more government "
            "power favors some at others' expense, the more rent seeking occurs.",
     'retired': True},
    # id 147 (retired)
    {'ch': 6,
     'q': 'Why do government-operated firms and agencies tend to be less efficient?',
     'opts': ['No profit motive to keep costs low and no bankruptcy process to weed out inefficient '
              'producers',
              'Government workers are less talented',
              'They face too much competition',
              'They are required to make a profit'],
     'exp': "Public managers rarely gain personally from cost cuts and spend other people's money, so "
            'they have less incentive to be cost-conscious.',
     'retired': True},
    # id 148 (retired)
    {'ch': 6,
     'q': 'Mattel helped write costly toy-testing rules into the 2008 Consumer Product Safety '
          "Improvement Act, raising smaller rivals' costs. This is an example of:",
     'opts': ['Crony capitalism', 'A public good', 'Comparative advantage', 'A positive externality'],
     'exp': 'Crony capitalism allocates resources by political favors rather than consumer '
            'preferences. Mattel gained while rivals and used-toy sellers like Goodwill were pushed '
            'out.',
     'retired': True},
    # id 149
    {'ch': 7,
     'q': 'Which definition of gross domestic product matches the one used in the course?',
     'opts': ['Market value of final goods and services produced inside a country in a period',
              'Market value of all goods sold inside a country in a period, new and used',
              "Market value of final goods and services produced by a country's citizens anywhere",
              'Market value of every intermediate and final good produced inside a country'],
     'exp': 'GDP is the market value of final goods and services produced within a country during a '
            'specific period, usually a year. Each part matters: final only, domestic production, and '
            'a set time period.',
     'why': [None,
             'Used goods were produced in an earlier period, so counting their resale would count past '
             'production again. GDP counts only current production of final goods and services.',
             'This defines output by citizenship. GDP is based on location: it counts what is produced '
             "inside the country's borders, regardless of who produces it, and leaves out citizens' "
             'production abroad.',
             'Adding intermediate goods double counts, because their value is already embodied in the '
             'final-user goods. Only final goods and services are summed.']},
    # id 150 (retired)
    {'ch': 7,
     'q': 'What are the two ways of measuring GDP?',
     'opts': ['The expenditure approach and the resource cost-income approach',
              'The CPI approach and the GDP deflator approach',
              'The micro approach and the macro approach',
              'The nominal approach and the real approach'],
     'exp': 'GDP measures both output and income: you can total spending on final goods, or total the '
            'incomes and costs generated by producing them.',
     'retired': True},
    # id 151 (retired)
    {'ch': 7,
     'q': 'In the expenditure approach, net exports equal:',
     'opts': ['Exports minus imports',
              'Imports minus exports',
              'Exports plus imports',
              'Exports minus government purchases'],
     'exp': 'The four components are consumption, gross private investment, government purchases, and '
            'net exports (exports minus imports).',
     'retired': True},
    # id 152
    {'ch': 7,
     'q': 'A clothing maker produces jackets this year that are still unsold in its warehouse on '
          'December 31. Under the expenditure approach, these jackets are recorded as:',
     'opts': ['Gross private investment, as an addition to inventories',
              'Consumption, because jackets are a consumer good',
              'Nothing yet, since they count in the year they are sold',
              'Net exports, because they were not sold at home'],
     'exp': 'Gross private investment includes changes in business inventories. Jackets produced this '
            'year but still unsold are counted this year as an addition to inventories, because GDP '
            'measures production in the period.',
     'why': [None,
             'The jackets have not been bought by households yet, so there is no consumption purchase '
             "this year. Until sold, they sit in the firm's inventory, which is part of investment.",
             "GDP counts production in the year it occurs. Waiting for the sale would miss this year's "
             'output, and the later sale from inventory is not new production.',
             'Net exports are exports minus imports. Unsold goods in a domestic warehouse have not '
             'been sold abroad, so they are not exports; they are an inventory addition.']},
    # id 153
    {'ch': 7,
     'q': 'Adding up employee compensation, self-employment income, rents, interest, and corporate '
          'profits gives:',
     'opts': ['National income', 'Nominal GDP', 'Personal consumption', 'Real GDP'],
     'exp': 'Employee compensation, self-employment income, rents, interest, and corporate profits are '
            'the direct cost-income components, and their sum is national income.',
     'why': [None,
             'Nominal GDP is larger: the resource cost-income approach also adds the indirect costs of '
             'producing goods and services, so these five components alone fall short of GDP.',
             'Personal consumption is a spending category from the expenditure approach, not a sum of '
             'incomes. These five items are payments to resource suppliers.',
             'Real GDP is GDP adjusted for inflation with a price index. Adding incomes produces no '
             'inflation adjustment, and the sum still omits indirect costs.']},
    # id 154 (retired)
    {'ch': 7,
     'q': "In GDP statistics, the term 'real' means:",
     'opts': ['Adjusted for inflation',
              'Measured in current dollars',
              'Including only physical goods',
              'Excluding government spending'],
     'exp': 'Real figures remove the effect of price changes so you can compare actual output across '
            'time.',
     'retired': True},
    # id 155 (retired)
    {'ch': 7,
     'q': 'A price index measures:',
     'opts': ['The cost of a market basket at a point in time relative to its cost in a base period',
              'The total quantity of goods produced',
              'The price of one specific product',
              'The interest rate on loans'],
     'exp': 'Price indexes like the CPI and GDP deflator compare the cost of the same bundle across '
            'periods to track inflation.',
     'retired': True},
    # id 156
    {'ch': 7,
     'q': 'How does the chained CPI differ from the traditional CPI?',
     'opts': ['It updates basket quantities monthly as buyers substitute away from pricier goods',
              'It expands the basket to include every final good and service counted in GDP',
              'It removes food and energy prices because those prices move around too much each month',
              'It keeps the same basket quantities for a decade to make comparisons more stable'],
     'exp': 'The chained CPI adjusts the quantities in the typical market basket each month to reflect '
            'shifts away from goods that have become relatively more expensive. That substitution '
            'adjustment is the key difference.',
     'why': [None,
             'Covering every final good and service in GDP describes the GDP deflator. The chained CPI '
             'is still a version of the CPI, built on the household bundle.',
             "Leaving out volatile food and energy prices is the idea behind 'core' inflation "
             'measures, not the chained CPI. The chained CPI keeps every household good and only '
             'updates quantities each month as buyers switch away from goods that got relatively more '
             'expensive.',
             'This describes the opposite of chaining. Keeping fixed quantities is what makes the '
             'traditional CPI miss substitution; the chained CPI updates quantities monthly.']},
    # id 157 (retired)
    {'ch': 7,
     'q': 'Compared with the traditional CPI, the chained CPI and GDP deflator generally show '
          'inflation that is:',
     'opts': ['About 0.2 to 0.3 percentage points lower',
              'About 2 to 3 percentage points higher',
              'Exactly the same',
              'About 5 percentage points lower'],
     'exp': 'More frequent updating of the bundle and substitution adjustments lead to slightly lower '
            'measured inflation.',
     'retired': True},
    # id 158 (retired)
    {'ch': 7,
     'q': 'Nominal GDP is $1,000 billion and the GDP deflator is 125 (base year = 100). Real GDP in '
          'base-year dollars is:',
     'opts': ['$800 billion', '$1,250 billion', '$875 billion', '$1,000 billion'],
     'exp': 'Real GDP = Nominal GDP x (base index / current index) = 1,000 x (100 / 125) = $800 '
            'billion.',
     'retired': True},
    # id 159 (retired)
    {'ch': 7,
     'q': "Your parents earned $40,000 in a year when the CPI was 100. The CPI is now 150. In today's "
          'dollars, their income equals:',
     'opts': ['$60,000', '$26,667', '$40,000', '$90,000'],
     'exp': 'Inflate earlier data: $40,000 x (150 / 100) = $60,000. This expresses old figures in '
            "today's purchasing power.",
     'retired': True},
    # id 160 (retired)
    {'ch': 7,
     'q': 'The GDP deflator rose from 120 to 126 over the year. The inflation rate was:',
     'opts': ['5%', '6%', '4.8%', '26%'],
     'exp': 'Inflation rate = (126 - 120) / 120 x 100 = 5%. Inflation can be calculated with either '
            'the CPI or the GDP deflator.',
     'retired': True},
    # id 161 (retired)
    {'ch': 7,
     'q': 'Income from illegal activities or hidden to avoid taxes is a GDP shortcoming known as:',
     'opts': ['The underground economy',
              'Nonmarket production',
              "Economic 'bads'",
              'Quality variation'],
     'exp': "Concealed activity isn't recorded, so GDP understates actual production.",
     'retired': True},
    # id 162 (retired)
    {'ch': 7,
     'q': 'Everyone works longer hours and takes less vacation, raising output. Why might GDP '
          'overstate the gain in well-being?',
     'opts': ['GDP excludes leisure and the human costs of production',
              'GDP counts leisure as output',
              'GDP subtracts wages',
              'GDP only counts government output'],
     'exp': 'GDP counts the extra goods but makes no deduction for the leisure given up or the strain '
            'of producing them.',
     'retired': True},
    # id 163 (retired)
    {'ch': 7,
     'q': "A factory's pollution harms a nearby community. How does GDP handle this?",
     'opts': ["It makes no adjustment for harmful side effects ('bads')",
              'It subtracts the damage from GDP',
              'It adds the damage to GDP',
              "It excludes the factory's output from GDP"],
     'exp': "GDP doesn't subtract harmful side effects of production, consumption, or destructive acts "
            'of people and nature.',
     'retired': True},
    # id 164
    {'ch': 7,
     'q': 'Free smartphone apps have replaced paid road maps, cameras, and music purchases. How does '
          'this affect GDP as a measure of well-being?',
     'opts': ['Well-being rises a lot, yet measured GDP grows little or even falls',
              'Measured GDP rises by the full retail value of the replaced products',
              'Measured GDP and well-being rise by about the same amount as before',
              'Well-being falls, because fewer goods are produced and sold in markets'],
     'exp': 'Information-age technology often improves well-being substantially while having less '
            'impact on GDP, and it can even reduce GDP when free products replace paid ones. GDP '
            'counts market sales, not the value people get.',
     'why': [None,
             'Free apps have no market price, so GDP records nothing for them. The maps, cameras, and '
             'music people no longer buy stop adding to measured output, so GDP can even fall.',
             'This assumes GDP tracks well-being one for one. In the information age, the gains to '
             'users rise much more than measured GDP does.',
             'Fewer market sales do not mean people are worse off. Users get the same or better '
             'services free, so well-being rises even though measured output may fall.']},
    # id 165 (retired)
    {'ch': 7,
     'q': 'Despite its shortcomings, real GDP per person is:',
     'opts': ['A broad indicator of living standards',
              'Unrelated to living standards',
              'A precise measure of happiness',
              'Only useful for measuring government size'],
     'exp': 'As real per capita GDP has risen, life expectancy and leisure rose while illiteracy and '
            'infant mortality fell.',
     'retired': True},
    # id 166 (retired)
    {'ch': 7,
     'q': 'Per capita GDP is calculated as:',
     'opts': ['GDP divided by the size of the population',
              'GDP divided by the number of workers',
              'GDP minus population',
              'GDP times the inflation rate'],
     'exp': 'In 2023, U.S. real per capita GDP was 3.4 times its 1960 level and 7.5 times its 1930 '
            'level.',
     'retired': True},
    # id 167 (retired)
    {'ch': 8,
     'q': 'Since 1960, the U.S. growth rate of real GDP has averaged approximately:',
     'opts': ['3% per year', '1% per year', '7% per year', '10% per year'],
     'exp': "Growth is about 3% a year on average, but it's unstable, with periodic recessions of "
            'declining real GDP.',
     'retired': True},
    # id 168
    {'ch': 8,
     'q': 'How does a depression differ from an ordinary recession?',
     'opts': ['It is a recession that is prolonged and very severe',
              'It is a recession in which prices rise instead of fall',
              'It is a slowdown in growth while real GDP keeps rising',
              'It is a recession confined to one industry or region'],
     'exp': 'A recession is a downturn with declining real GDP and rising unemployment. A depression '
            'is a recession that is prolonged and very severe; the difference is length and depth.',
     'why': [None,
             'The distinction is severity and duration, not the direction of prices. A depression is '
             'defined by how deep and long the downturn is.',
             'A recession requires real GDP to decline. A slowdown with real GDP still rising is not a '
             'recession, let alone a depression.',
             'A depression is an economy-wide downturn, not a slump in one industry or region. It is a '
             'recession that is prolonged and very severe.']},
    # id 169 (retired)
    {'ch': 8,
     'q': 'When most businesses operate at capacity and real GDP is growing rapidly, the economy is at '
          'a:',
     'opts': ['Peak (boom)', 'Recessionary trough', 'Contraction', 'Depression'],
     'exp': 'After the peak, business conditions slow and the contraction (recessionary) phase begins.',
     'retired': True},
    # id 170 (retired)
    {'ch': 8,
     'q': 'A person who is not working but applied for a job at Target last week is:',
     'opts': ['Unemployed', 'Employed', 'Not in the labor force', 'Discouraged and not counted'],
     'exp': 'Actively seeking a job while not working counts as unemployed.',
     'retired': True},
    # id 171 (retired)
    {'ch': 8,
     'q': 'A homemaker working 70 hours a week preparing meals and doing household tasks is classified '
          'as:',
     'opts': ['Not in the labor force', 'Employed', 'Unemployed', 'Self-employed'],
     'exp': "Household production isn't paid market work, so the homemaker isn't counted as employed "
            'or unemployed.',
     'retired': True},
    # id 172
    {'ch': 8,
     'q': 'Which of these people is counted as employed?',
     'opts': ["A teen working 18 unpaid hours a week in her family's restaurant",
              "A teen working 8 unpaid hours a week in his family's restaurant business",
              'A retiree who volunteers 20 hours a week at a local hospital',
              'A student who has accepted a job that begins early next month'],
     'exp': 'Unpaid work in a family-operated enterprise counts as employment at 15 or more hours a '
            'week. The teen working 18 unpaid hours meets that threshold.',
     'why': [None,
             'Eight unpaid hours falls short of the 15-hour threshold for unpaid family work, so this '
             'teen is not counted as employed.',
             'Volunteering is not work for pay or in a family enterprise. The retiree is not employed '
             'and is not in the labor force.',
             'A person waiting to begin a job is counted as unemployed, not employed, until the job '
             'actually starts.']},
    # id 173 (retired)
    {'ch': 8,
     'q': 'Population age 16+ = 250M and employed = 152M. The employment-population ratio is:',
     'opts': ['60.8%', '64%', '95%', '5%'],
     'exp': 'Employment-population ratio = employed / population 16+ = 152 / 250 = 60.8%.',
     'retired': True},
    # id 174 (retired)
    {'ch': 8,
     'q': 'Unemployment that rises because of a general downturn in business activity is:',
     'opts': ['Cyclical unemployment',
              'Frictional unemployment',
              'Structural unemployment',
              'Seasonal unemployment'],
     'exp': "Cyclical unemployment reflects business cycle conditions. It's absent at full employment.",
     'retired': True},
    # id 175 (retired)
    {'ch': 8,
     'q': 'Which factors influence the natural rate of unemployment?',
     'opts': ['Demographics (like the share of young workers) and public policy (like unemployment '
              'benefits)',
              'Only the money supply',
              'Only the inflation rate',
              "Nothing; it's fixed forever"],
     'exp': "The natural rate reflects job shopping in a dynamic economy. It's achievable and "
            'sustainable, and it changes with demographics and policy.',
     'retired': True},
    # id 176 (retired)
    {'ch': 8,
     'q': 'True or false: when full employment is present, the unemployment rate will be zero.',
     'opts': ['False: frictional and structural unemployment remain',
              'True: everyone has a job',
              'True: only cyclical unemployment remains',
              'False: cyclical unemployment is at its highest'],
     'exp': 'Full employment means unemployment is at its natural rate, with normal job search and '
            'skill mismatches still present.',
     'retired': True},
    # id 177
    {'ch': 8,
     'q': 'Potential output is best described as:',
     'opts': ['The highest output the economy can sustain given its resources and institutions',
              'The highest output the economy has ever reached, even for a short-lived boom period',
              'The output the economy would produce if the unemployment rate fell to zero',
              'The output the economy produces in a typical year once inflation is removed'],
     'exp': "Potential output is the maximum sustainable output consistent with the economy's resource "
            'base and institutional arrangements. It is reached at full employment.',
     'why': [None,
             'A short-lived boom can push output above potential temporarily. Potential output is the '
             'maximum level that can be sustained, not the record high.',
             'Potential output corresponds to full employment, where the natural rate of unemployment '
             'remains. Zero unemployment is neither achievable nor sustainable.',
             'Removing inflation gives real GDP, which is actual output. Potential output is the '
             'sustainable maximum, which actual output can be above or below.']},
    # id 178 (retired)
    {'ch': 8,
     'q': 'According to economists, what causes inflation?',
     'opts': ['Aggregate demand rising faster than supply, and rapid growth of the money supply',
              'Falling aggregate demand',
              'Low unemployment benefits',
              'Rising productivity'],
     'exp': "Prices rise when there is 'too much money chasing too few goods.' Nearly all economists "
            'link rapid money growth to inflation.',
     'retired': True},
    # id 179 (retired)
    {'ch': 9,
     'q': 'Which is NOT one of the four key markets that coordinate the circular flow?',
     'opts': ['The housing market',
              'The goods and services market',
              'The loanable funds market',
              'The foreign exchange market'],
     'exp': 'The four markets are goods and services, resources, loanable funds, and foreign exchange.',
     'retired': True},
    # id 180
    {'ch': 9,
     'q': 'To fight a recession, a central bank deliberately expands the quantity of currency and '
          'checking account funds in the economy. Which statement is correct?',
     'opts': ['This is monetary policy, since it deliberately changes the means of payment people use',
              'This is fiscal policy, since the government is acting to reach a macroeconomic goal',
              'This is monetary policy, since it works by changing tax rates and government spending',
              'This is fiscal policy, since checking account funds are not counted in the money '
              'supply'],
     'exp': 'Currency and checking account funds are part of the money supply because they serve as '
            'the means of payment. Deliberately changing the money supply to reach a macroeconomic '
            'goal is monetary policy.',
     'why': [None,
             'Fiscal policy uses taxes and government spending. Having a macroeconomic goal does not '
             'make a policy fiscal; the tool used, here the money supply, decides the label.',
             "The label is right, but the reason gives fiscal policy's tools. Monetary policy works by "
             'controlling the money supply, not tax rates and spending.',
             'Checking account funds are counted in the money supply, along with currency and '
             "traveler's checks, so changing them is monetary policy."]},
    # id 181 (retired)
    {'ch': 9,
     'q': 'The aggregate demand curve shows:',
     'opts': ['The quantities of domestically produced goods and services buyers will purchase at '
              'different price levels',
              'The total supply of goods at each price level',
              'The demand for money at each interest rate',
              'Demand for imported goods only'],
     'exp': 'AD slopes downward: a lower price level means a larger quantity of goods and services '
            'demanded.',
     'retired': True},
    # id 182
    {'ch': 9,
     'q': 'In the AD–AS model, what distinguishes the short run from the long run?',
     'opts': ['In the short run some prices, especially resource prices, are fixed by prior contracts',
              'In the short run resources and technology are fixed, but every price is flexible',
              'In the short run prices adjust quickly, while in the long run contracts lock them in '
              'place',
              'In the short run output is held at YF, while in the long run it can exceed YF'],
     'exp': 'The short run is a period when some prices, especially resource prices, are set by prior '
            'contracts, so people cannot adjust to unexpected changes in the price level. The long run '
            'is long enough for people to modify their behavior.',
     'why': [None,
             'In this model the short run is defined by contract-fixed prices, not by fixed resources '
             'and technology. Saying every price is flexible removes the feature that defines it.',
             'This reverses the two periods. Contracts lock in prices in the **short** run; in the '
             'long run people have time to renegotiate them.',
             'This is backward. Output can temporarily exceed YF in the short run, but in the long run '
             'it returns to YF, the largest sustainable output rate.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD'},
                       {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS'},
                       {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
             'points': [{'at': [50, 50], 'label': 'E'}],
             'guides': True,
             'xticks': [[50, 'YF']],
             'yticks': [[50, 'P1']],
             'alt': 'A downward-sloping AD curve, an upward-sloping SRAS curve, and a vertical LRAS '
                    'line all pass through point E at full-employment output YF and price level P1.'}},
    # id 183 (retired)
    {'ch': 9,
     'q': 'If the price level is ABOVE the short-run equilibrium level (where AD meets SRAS):',
     'opts': ['Excess supply will push prices down',
              'Excess demand will push prices up',
              'Output will rise to meet demand',
              'The economy is in long-run equilibrium'],
     'exp': 'Above equilibrium, sellers want to supply more than buyers want, so prices fall. Below '
            'it, excess demand pushes prices up.',
     'retired': True},
    # id 184
    {'ch': 9,
     'q': 'In the United States, labor costs make up roughly what share of total production costs?',
     'opts': ['About 70%', 'About 30%', 'About 50%', 'About 90%'],
     'exp': 'Labor is by far the largest part of the resource market, making up roughly 70% of U.S. '
            'production costs.',
     'why': [None,
             "About 30% is closer to the share left for all other inputs combined. Labor's share is "
             'much larger, about 70%.',
             "Half understates labor's role. Capital and raw materials matter, but labor makes up "
             'roughly 70% of production costs.',
             'This overstates it. Labor dominates, but other inputs still account for roughly 30% of '
             'costs, leaving labor at about 70%.']},
    # id 185 (retired)
    {'ch': 9,
     'q': "From a lender's viewpoint, interest is:",
     'opts': ['A premium received for waiting (delaying current spending)',
              'The cost paid for earlier availability',
              'A tax paid to the government',
              'The inflation rate'],
     'exp': "For borrowers, interest is the cost of getting funds earlier. For lenders, it's the "
            'reward for waiting.',
     'retired': True},
    # id 186 (retired)
    {'ch': 9,
     'q': 'The difference between the money interest rate and the real interest rate is the:',
     'opts': ['Inflationary premium', 'Risk premium', 'Exchange rate', 'Profit margin'],
     'exp': "The inflationary premium reflects the expected decline in the dollar's purchasing power "
            'while the loan is outstanding.',
     'retired': True},
    # id 187 (retired)
    {'ch': 9,
     'q': 'If actual inflation turns out LOWER than anticipated:',
     'opts': ['Lenders gain at the expense of borrowers',
              'Borrowers gain at the expense of lenders',
              'Neither gains nor loses',
              'Both gain equally'],
     'exp': 'Borrowers repay with dollars worth more than expected, and the inflation premium they '
            'paid turns out too high.',
     'retired': True},
    # id 188 (retired)
    {'ch': 9,
     'q': 'When domestic demand for loanable funds is weak and the real interest rate is low:',
     'opts': ['Capital flows out toward markets with higher expected returns',
              'Capital flows in from abroad',
              'Interest rates must rise immediately',
              'The trade deficit grows'],
     'exp': 'Investors seek the best returns globally. Strong domestic demand and high rates attract a '
            'capital inflow instead.',
     'retired': True},
    # id 189 (retired)
    {'ch': 9,
     'q': 'In recent years, much of the capital inflow to the U.S. has financed federal deficits. The '
          'result has been:',
     'opts': ['Higher current consumption and lower investment, slowing growth',
              'Higher investment and faster growth',
              'A trade surplus',
              'Lower federal spending'],
     'exp': 'Borrowing to support current consumption reduces capital formation. Like a family, a '
            "nation can't solve financial problems by borrowing more to keep consuming.",
     'retired': True},
    # id 190 (retired)
    {'ch': 9,
     'q': 'If the U.S. dollar appreciates against the euro:',
     'opts': ['Fewer dollars are needed to buy a euro, and net exports tend to fall',
              'More dollars are needed to buy a euro, and net exports rise',
              'Fewer dollars are needed to buy a euro, and net exports rise',
              'Nothing happens to net exports'],
     'exp': 'A stronger dollar makes foreign goods cheaper for Americans and U.S. goods pricier for '
            'foreigners, so imports rise and exports fall.',
     'retired': True},
    # id 191 (retired)
    {'ch': 9,
     'q': 'If the inflation rate increases and stays higher for a long time, what happens to interest '
          'rates?',
     'opts': ['The nominal rate rises; the real rate stays about the same',
              'The real rate rises; the nominal rate stays the same',
              'Both fall',
              'Neither changes'],
     'exp': 'Once higher inflation is expected, lenders add a bigger inflation premium (e.g., 6% real '
            '+ 5% expected inflation = 11% nominal).',
     'retired': True},
    # id 192
    {'ch': 10,
     'q': 'Which best describes an **anticipated** change in the macroeconomy?',
     'opts': ['One that people foresee and can adjust their contracts to before it occurs',
              'One that catches people by surprise after their contracts have been signed',
              'One that shifts the LRAS curve rather than the AD or SRAS curves',
              'One that the government announces after it has already taken place'],
     'exp': 'Anticipated changes are fully expected, so decision makers have time to adjust their '
            'contracts and plans before the changes occur. That is why anticipated changes need not '
            'disrupt equilibrium.',
     'why': [None,
             'A change that surprises people after they have signed contracts is an **unanticipated** '
             'change, the kind that disrupts equilibrium.',
             'Anticipation is about whether people foresee a change, not which curve it moves. Changes '
             'in AD or SRAS can be anticipated too.',
             'A change announced only after it happens gives people no time to adjust beforehand, so '
             'it would be unanticipated.']},
    # id 193 (retired)
    {'ch': 10,
     'q': 'An increase in the EXPECTED rate of inflation will tend to:',
     'opts': ['Increase aggregate demand',
              'Decrease aggregate demand',
              'Shift LRAS to the right',
              'Have no effect on AD'],
     'exp': 'If people expect prices to rise, they buy more now, shifting AD right. Expected inflation '
            'also reduces SRAS, since resource costs rise.',
     'retired': True},
    # id 194 (retired)
    {'ch': 10,
     'q': 'Higher real incomes in other countries will:',
     'opts': ['Increase U.S. aggregate demand, since foreigners buy more U.S. exports',
              'Decrease U.S. aggregate demand',
              'Shift U.S. LRAS left',
              'Have no effect on the U.S.'],
     'exp': 'Richer foreigners demand more U.S. goods, raising net exports and AD.',
     'retired': True},
    # id 195 (retired)
    {'ch': 10,
     'q': 'A reduction in EXPECTED inflation would:',
     'opts': ['Shift SRAS to the right, without changing LRAS',
              'Shift LRAS to the right',
              'Shift both LRAS and SRAS to the left',
              'Shift AD to the right'],
     'exp': 'SRAS shifters include resource prices, expected inflation, and supply shocks. LRAS '
            'depends on resources, technology, and institutions. It would also tend to shift AD to the '
            'left, not right, since lower expected inflation reduces current buying.',
     'retired': True},
    # id 196 (retired)
    {'ch': 10,
     'q': 'If an adverse supply shock (like a higher oil price) turns out to be PERMANENT:',
     'opts': ["LRAS shifts left and the economy's productive potential shrinks",
              'The economy returns to its original equilibrium',
              'LRAS shifts right',
              'Only AD is affected'],
     'exp': 'A temporary shock fades as resource prices fall back. A permanent one reduces potential '
            'output, so LRAS shifts left.',
     'retired': True},
    # id 197
    {'ch': 10,
     'q': 'When the actual rate of inflation equals the expected rate, what happens to prices in '
          'resource and product markets?',
     'opts': ['Both rise, and the relative price between them stays unchanged',
              "Product prices rise faster, so firms' profit margins widen",
              "Resource prices rise faster, so firms' profit margins shrink",
              'Both stay constant, because long-term contracts prevent price changes'],
     'exp': 'When actual inflation equals expected inflation, it is built into long-term contracts. '
            'Prices rise in both resource and product markets, so the relative price between them, and '
            "firms' profit margins, stay unchanged.",
     'why': [None,
             'Margins widen only when actual inflation **exceeds** expected inflation. Correctly '
             'expected inflation is already built into costs.',
             'Margins shrink only when actual inflation falls **short** of expected inflation. Here '
             'the two rates are equal.',
             'Contracts do not freeze prices; they build the expected inflation in, so prices rise in '
             'both markets at the expected rate.']},
    # id 198 (retired)
    {'ch': 10,
     'q': 'According to the AD-AS model, the two causes of economic BOOMS are:',
     'opts': ['Unanticipated increases in AD and favorable supply shocks',
              'Anticipated increases in AD and higher taxes',
              'Higher resource prices and lower real wealth',
              'Unfavorable supply shocks and falling AD'],
     'exp': 'Booms happen when goods prices are high relative to resource prices and costs. Recessions '
            'are the mirror image.',
     'retired': True},
    # id 199 (retired)
    {'ch': 10,
     'q': "After a temporary favorable supply shock, people who know their high income won't last tend "
          'to:',
     'opts': ['Save more, which can lower interest rates and boost capital formation',
              'Spend all of the extra income immediately',
              'Borrow more',
              'Stop working'],
     'exp': 'Since the higher income is temporary, saving rises. With an unfavorable shock, households '
            'may dip into past savings instead.',
     'retired': True},
    # id 200
    {'ch': 1,
     'q': 'A town keeps a downtown lot as open space. A developer had offered $3 million to build '
          'apartments there, and a hospital had offered $2 million for a clinic site. What is the '
          'opportunity cost of keeping the open space?',
     'opts': ['The apartment project, the most valuable use that was given up',
              'The mowing and upkeep, the money the town actually spends on it',
              '$5 million, the total of both offers that the town turned down',
              'The clinic, because it would serve the most people in the town'],
     'exp': 'Guidepost 1: no option is free, and the opportunity cost is the highest-valued '
            'alternative sacrificed. The town could have accepted only one offer, and the $3 million '
            'apartment project was the most valuable.',
     'why': [None,
             'Upkeep spending is a money cost of the choice, but opportunity cost is the '
             'highest-valued alternative given up, which here is the $3 million apartment use.',
             'Adding the two offers counts two alternatives, but the town could have accepted only '
             'one. Only the highest-valued forgone use counts.',
             'Serving more people is a value judgment, not the value the offers place on each use. By '
             'the offers, the apartment use was valued highest.']},
    # id 201
    {'ch': 1,
     'q': "Maria can get to the airport by rideshare for $40, by shuttle for $15, or by a friend's "
          'free ride that means leaving 3 hours early and waiting. She takes the shuttle. A classmate '
          "says she acted irrationally because the friend's ride was free. What is wrong with the "
          "classmate's reasoning?",
     'opts': ['The free ride costs 3 hours of her time, so it may not be cheapest',
              "It's correct; economizing means choosing the option with the lowest price",
              'Economizing behavior describes business firms, not individual travelers',
              "Travel choices rest on subjective value, so they can't be compared"],
     'exp': 'Economizing behavior means getting the most from limited resources, and time is a scarce '
            'resource too. Once her three hours of waiting are valued, the free ride may cost more '
            'than the $15 shuttle.',
     'why': [None,
             "Economizing doesn't mean picking the lowest money price. It means getting the most from "
             'all limited resources, including the time the free ride uses up.',
             'Economizing behavior applies to everyone who makes choices. Guidepost 2 says individuals '
             'choose purposefully to get the most from their limited resources.',
             'Value is subjective, but people still compare options and choose among them. Her choice '
             'can be analyzed by counting all its costs, including time.']},
    # id 202
    {'ch': 1,
     'q': 'A university wants more students in its 8 a.m. classes and is considering two ideas. '
          'Statement I: Letting 8 a.m. students register early is unlikely to change which classes '
          'students choose. Statement II: Raising parking fees during midday hours could lead some '
          'students to switch into 8 a.m. classes.',
     'opts': ['I is false and II is true',
              'I is true and II is false',
              'I is true and II is true',
              'I is false and II is false'],
     'exp': "Guidepost 3: incentives matter, and they don't have to be money. Early registration is "
            'valuable to students, so it can shift their choices, which makes Statement I false. '
            'Statement II is true because raising the cost of the alternative, midday classes, makes 8 '
            'a.m. classes relatively more attractive.',
     'why': [None,
             'Both statements were misjudged. Early registration is a nonmonetary incentive that can '
             'change class choices, so I is false; and higher midday parking fees make 8 a.m. classes '
             'relatively cheaper, so II is true.',
             "Statement I is false. Incentives don't need to involve money: early registration is "
             'valuable to students, so offering it can change which classes they choose.',
             'Statement II is true. Raising the cost of parking for midday classes makes the 8 a.m. '
             'alternative relatively more attractive, so some students will switch.']},
    # id 203
    {'ch': 1,
     'q': 'A bakery already makes 200 loaves a day. Making a 201st loaf would add $1.50 to its costs. '
          "The bakery's average cost per loaf is $2.00, and the extra loaf would sell for $1.80. "
          'Should the bakery make the extra loaf?',
     'opts': ['Yes, because the extra loaf adds more to revenue than to cost',
              'No, because the $1.80 price is below the $2.00 average cost',
              "No, because it should first cover its total cost for the day's loaves",
              'Yes, because any loaf sold at a positive price raises its profit'],
     'exp': 'Decisions are made at the margin. The 201st loaf adds $1.80 to revenue and $1.50 to cost, '
            'so making it raises profit by $0.30.',
     'why': [None,
             "Average cost includes all the earlier loaves, which this decision doesn't change. The "
             "relevant comparison is the extra loaf's $1.50 added cost against its $1.80 price.",
             'The cost of the first 200 loaves is already set either way. The decision depends only on '
             'what the 201st loaf adds to revenue and to cost.',
             "A positive price isn't enough. A loaf raises profit only if its price exceeds the cost "
             'it adds; $1.80 beats $1.50 here, but a $1.20 price would not.']},
    # id 204
    {'ch': 1,
     'q': 'Jordan checked the price of a used laptop at three websites and bought the cheapest one. '
          'Later he learned a fourth site had it for $20 less. A friend says Jordan made an irrational '
          'choice. What is the best response?',
     'opts': ['More searching takes scarce time, so stopping early can be sensible',
              'Jordan erred; a rational buyer searches until finding the lowest price',
              "Jordan's choice reflects subjective value, so it can't be evaluated",
              'Jordan ignored the secondary effects his purchase had on other buyers'],
     'exp': 'Guidepost 5: information helps us choose, but gathering it takes scarce time. At some '
            "point more comparison shopping isn't worth the trouble, so stopping after three sites can "
            'be a sensible choice.',
     'why': [None,
             'This ignores that searching has a cost of its own. A rational buyer stops when another '
             "search isn't expected to be worth the time it takes.",
             'Value is subjective, but choices can still be analyzed by comparing costs and benefits, '
             'including the cost of gathering more information.',
             "Secondary effects are indirect consequences of actions or policies; they don't explain "
             'why Jordan stopped searching. The issue is the cost of acquiring information.']},
    # id 205
    {'ch': 1,
     'q': 'A city bans plastic grocery bags and reports less litter. Two years later, studies link '
          'heavily reused cloth bags to the spread of bacteria. Why do consequences like this tend to '
          'be missed when policies are adopted?',
     'opts': ['They are indirect and may not be easily or immediately observed',
              'They are normative judgments that economists are unable to measure',
              "They are typically much smaller than a policy's direct effects",
              'They come from voluntary choices, which policy cannot influence'],
     'exp': 'This is a secondary effect: an indirect impact that may not be easily and immediately '
            'observed. In policy, such effects are often unintended and overlooked, as in the '
            'plastic-bag example from the slides.',
     'why': [None,
             'Whether reused bags spread bacteria is a testable claim about what is, so it is '
             'positive, not normative, and can be studied with evidence.',
             "Secondary effects aren't necessarily smaller than direct effects. They are missed "
             'because they are indirect and hard to see, not because they are minor.',
             'Policies change incentives and so do influence voluntary choices; switching to cloth '
             'bags is exactly such a response. The effect is missed because it is indirect.']},
    # id 206
    {'ch': 1,
     'q': 'A seller who valued a vintage guitar at $5,000 sells it to a collector for $8,000. The '
          'collector would have paid up to $9,000. Which statement is correct?',
     'opts': ['The guitar is worth different amounts to each, so both can gain',
              "The guitar's true value is $8,000, so the seller was shortchanged",
              "The guitar's value is set by its physical condition and its age",
              'The sale just moved value around, since the guitar did not change'],
     'exp': 'Guidepost 7: value is subjective and varies with individual preferences. The seller gains '
            '$3,000 over her $5,000 value and the collector gains $1,000 under his $9,000 limit, so '
            'the trade creates value for both.',
     'why': [None,
             'Treating the sale price as a true value ignores that value differs by person. The seller '
             'valued the guitar at $5,000, so selling at $8,000 made her better off.',
             'Physical traits matter, but value also depends on who uses a good and the circumstances. '
             'The same guitar was worth $5,000 to one person and $9,000 to another.',
             'Trade creates value by moving a good to someone who values it more, even though the good '
             'itself is unchanged. Both parties gained here.']},
    # id 207
    {'ch': 1,
     'q': 'Two models forecast housing prices. Model A uses very simplified assumptions but has '
          'predicted price changes accurately for 15 years. Model B uses highly realistic assumptions, '
          'but its forecasts have repeatedly been far off. Which model does the economic way of '
          'thinking favor?',
     'opts': ['Model A, because a theory is judged by how well it predicts',
              'Model B, because a theory is judged by realistic assumptions',
              "Neither, because economic theories can't be tested like science",
              'Model B, because experts tend to prefer more detailed models'],
     'exp': "Guidepost 8: the test of a theory is its ability to predict. Model A's 15-year record of "
            'accurate forecasts passes that test, even though its assumptions are simplified.',
     'why': [None,
             "Realistic assumptions aren't the test. A model whose forecasts are repeatedly far off "
             'fails the test that matters, which is prediction.',
             'Economic thinking is scientific thinking: theories are tested against real-world events, '
             "and both models' forecasts can be checked that way.",
             "A preference for detail isn't the scientific test. A theory is judged by how well it "
             'predicts, and Model B predicts poorly.']},
    # id 208
    {'ch': 1,
     'q': 'Statement I: "Raising the minimum wage to $20 would reduce teen employment" is a positive '
          'statement. Statement II: "Workers deserve a $20 minimum wage" is a positive statement '
          'because data on wages can be used to debate it.',
     'opts': ['I is true and II is false',
              'I is true and II is true',
              'I is false and II is true',
              'I is false and II is false'],
     'exp': 'Statement I is a cause-and-effect claim that evidence could check, so it is positive even '
            "if it turns out wrong. Statement II is a judgment about what workers deserve, which can't "
            'be proved true or false, so it is normative.',
     'why': [None,
             'Statement II was misjudged. Having wage data doesn\'t make "workers deserve" testable; '
             'it is a value judgment about what ought to be, so it is normative.',
             'Both were misjudged. Statement I is positive because its predicted effect could be '
             'checked against evidence, and Statement II is normative because "deserve" is a value '
             'judgment.',
             'Statement I was misjudged. A prediction about teen employment is potentially verifiable, '
             'so it is positive even if you think it is wrong.']},
    # id 209
    {'ch': 1,
     'q': 'A classmate says, "The claim that a tax cut will triple tax revenue next year is clearly '
          'false, so it must be a normative statement." What is wrong with this reasoning?',
     'opts': ["A positive statement can be false; what counts is whether it's testable",
              "It's correct; statements that are shown to be false are classed as normative",
              'The claim is normative because it is about government tax policy',
              'The claim is neither, since it is a prediction about the future'],
     'exp': 'Positive statements are about what is and are potentially verifiable, but they are not '
            'necessarily correct. A claim about future tax revenue can be checked, so even a false one '
            'is still positive.',
     'why': [None,
             "Being false doesn't make a statement normative. Normative statements are value judgments "
             "that can't be proved true or false at all; a false testable claim is still positive.",
             "A policy topic doesn't make a claim normative. Predicting revenue is testable; only "
             'judgments about what ought to be are normative.',
             'Predictions about the future are positive statements, because they can be checked '
             'against what actually happens.']},
    # id 210
    {'ch': 1,
     'q': 'In a year when the price of beef rose, people also bought more beef than the year before. A '
          'student concludes that higher prices cause people to buy more beef. What is the most likely '
          'flaw?',
     'opts': ["Other factors such as incomes changed too, so they weren't held constant",
              'The student moved from one buyer to every buyer, a fallacy of composition',
              "The student's claim is normative, so it can't be checked with evidence",
              'The student forgot that information about beef prices is costly to get'],
     'exp': 'Ceteris paribus means other things constant. If incomes or tastes also changed that year, '
            'the larger beef purchases may reflect those factors rather than the higher price.',
     'why': [None,
             "The student isn't reasoning from one buyer to the group; the data already cover all "
             'buyers. The flaw is failing to hold other factors constant.',
             'Whether higher prices lead people to buy more is a claim about what is, so it is '
             'positive and can be tested with evidence.',
             "The cost of information isn't the issue. The conclusion fails because other factors "
             "affecting beef purchases weren't held constant."]},
    # id 211
    {'ch': 1,
     'q': 'Wanting to help low-income renters, a city council passes a policy that ends up shrinking '
          'the supply of apartments. A council member responds, "Our hearts were in the right place, '
          'so the policy can\'t be blamed." What mistake is the council member making?',
     'opts': ['Assuming that good motives ensure good results from a policy',
              'Assuming that what helps one renter will help renters as a group',
              'Assuming that two events happening together means one caused the other',
              'Assuming a policy can be judged without holding other things constant'],
     'exp': 'Good intentions do not guarantee desirable outcomes: an unsound proposal causes harm even '
            'when its supporters mean well. The council member is judging the policy by its motives '
            'rather than its results.',
     'why': [None,
             'That describes the fallacy of composition, reasoning from one part to the whole. The '
             'council member is arguing from motives, not from one renter to all renters.',
             "That is the association-versus-causation pitfall. The council member doesn't dispute "
             'what caused the result; he excuses the policy because of its goals.',
             'A ceteris paribus error means failing to hold other factors constant. The council '
             "member's mistake is assuming good motives excuse bad results."]},
    # id 212
    {'ch': 1,
     'q': 'Students who use the campus tutoring center have lower average grades than students who '
          'don\'t. A dean proposes closing the center because tutoring "hurts grades." What is the '
          'best critique?',
     'opts': ['Struggling students are more likely to seek tutoring',
              "The dean assumes what's true for one student is true for all students",
              "The dean's claim is normative, so grade data can't test it",
              'Grades have subjective value that differs for each student'],
     'exp': 'Statistical association alone cannot establish causation. Students who are struggling are '
            'more likely to seek tutoring, so low grades may lead to tutoring rather than tutoring '
            'causing low grades.',
     'why': [None,
             "The dean isn't generalizing from one student to all; he's drawing a causal conclusion "
             'from group data. The flaw is treating association as causation.',
             '"Tutoring hurts grades" is a claim about what is, so it is positive and evidence can '
             'test it. The problem is how the evidence was interpreted.',
             "Subjective value doesn't address the flaw. A link between tutoring and lower grades "
             "doesn't prove that tutoring causes the lower grades."]},
    # id 213
    {'ch': 1,
     'q': 'At a concert, one fan who stands up gets a better view. Someone concludes that if everyone '
          'stands, everyone will see better. Which statement best explains the error?',
     'opts': ['What benefits one person acting alone may not benefit the whole group',
              'The conclusion confuses a statistical association with a true cause',
              "The conclusion fails to hold factors like the stage's height constant",
              "The conclusion is a normative claim that can't be tested with data"],
     'exp': "This is the fallacy of composition: what is true for one part isn't necessarily true for "
            "the whole. If everyone stands, no one's view improves.",
     'why': [None,
             'Association versus causation is about inferring cause from two things moving together. '
             "Here the error is assuming one person's gain carries over to the whole group.",
             'Nothing else has changed here; the stage is the same height either way. The error is '
             'reasoning from one fan to every fan.',
             'Whether everyone sees better when all stand is a claim about what is, so it is positive '
             'and could be tested.']},
    # id 214
    {'ch': 1,
     'q': 'Tickets to a popular concert are sold at a price well below what fans would pay, on a '
          'first-come, first-served basis. Compared with letting price ration the tickets, what is the '
          'most likely result?',
     'opts': ['Tickets go to those willing to wait longest, and fans spend time in line',
              'Scarcity disappears, because every fan who wants a ticket can afford one',
              'Tickets go to the fans willing to give up the most other goods for them',
              'Fans gain a stronger incentive to earn more income to buy the tickets'],
     'exp': 'Every society must ration scarce goods; a below-market price just changes the method. '
            'With first-come, first-served, tickets go to those willing to wait longest, so fans pay '
            'in time instead of money.',
     'why': [None,
             "A low price doesn't end scarcity: more fans want tickets than there are seats, so some "
             'other method, here waiting, decides who gets them.',
             'Going to those willing to give up the most other goods describes price rationing, which '
             'is exactly what the low price prevents here.',
             'The incentive to earn income comes from price rationing. When waiting in line decides '
             "who gets tickets, extra income doesn't help much."]},
    # id 215
    {'ch': 2,
     'q': 'Use the graph. Which statement about points A, B, and C is correct?',
     'opts': ['A is efficient, B is attainable but inefficient, and C is unattainable',
              'A is efficient, B is unattainable, and C is attainable but inefficient',
              'A and B are both efficient, while C is unattainable with current resources',
              'B is efficient, A is attainable but inefficient, and C is unattainable'],
     'exp': 'Points on the curve, like A, are efficient. Point B is inside the curve, so the economy '
            'could get more food with the same clothing: it is attainable but inefficient. Point C '
            'lies beyond the curve and cannot be reached with current resources and technology.',
     'why': [None,
             'This swaps B and C. B lies inside the curve, so it can be reached; C lies outside, so it '
             "can't be produced with current resources.",
             'Only points on the curve are efficient. B lies inside, so more of one good could be '
             'produced without giving up any of the other.',
             'This swaps A and B. A is on the curve, so it is efficient; B lies inside, where '
             'resources are not fully or efficiently used.'],
     'fig': {'type': 'graph',
             'x': 'Clothing',
             'y': 'Food',
             'lines': [{'pts': [[8, 88], [30, 84], [50, 74], [66, 58], [78, 38], [85, 8]],
                        'cls': 's',
                        'label': 'PPC'}],
             'points': [{'at': [66, 58], 'label': 'A'},
                        {'at': [38, 45], 'label': 'B'},
                        {'at': [72, 78], 'label': 'C'}],
             'guides': False,
             'alt': 'A bowed-out production possibilities curve with food on the vertical axis and '
                    'clothing on the horizontal axis. Point A lies on the curve, point B lies below '
                    'and to the left of the curve, and point C lies above and to the right of the '
                    'curve.'}},
    # id 216
    {'ch': 2,
     'q': 'Use the graph. When the economy moves from point B to point C, what is the opportunity cost '
          'of each additional computer?',
     'opts': ['3 units of wheat', '1 unit of wheat', '6 units of wheat', '1/3 unit of wheat'],
     'exp': 'From B to C, computers rise by 10, from 10 to 20, while wheat falls by 30, from 90 to 60. '
            'Each added computer therefore costs 30 / 10 = 3 units of wheat.',
     'why': [None,
             '1 unit is the cost per computer from A to B, where wheat falls only 10. The B-to-C '
             'segment has wheat falling by 30.',
             '6 units is the cost per computer from C to D, where wheat falls 60. The question asks '
             'about the move from B to C.',
             'This flips the ratio: 10 computers per 30 wheat is computers per unit of wheat. The cost '
             'of a computer is wheat lost divided by computers gained.'],
     'fig': {'type': 'graph',
             'x': 'Computers',
             'y': 'Wheat (units)',
             'lines': [{'pts': [[10, 85], [35, 77.5], [60, 55], [85, 10]], 'cls': 's', 'label': 'PPC'}],
             'points': [{'at': [10, 85], 'label': 'A'},
                        {'at': [35, 77.5], 'label': 'B'},
                        {'at': [60, 55], 'label': 'C'},
                        {'at': [85, 10], 'label': 'D'}],
             'guides': True,
             'xticks': [[10, '0'], [35, '10'], [60, '20'], [85, '30']],
             'yticks': [[10, '0'], [55, '60'], [77.5, '90'], [85, '100']],
             'alt': 'A bowed-out production possibilities curve for computers on the horizontal axis '
                    'and wheat on the vertical axis. Point A is 0 computers and 100 wheat, point B is '
                    '10 computers and 90 wheat, point C is 20 computers and 60 wheat, and point D is '
                    '30 computers and 0 wheat.'}},
    # id 217
    {'ch': 2,
     'q': 'Use the graph. Statement I: Moving from A to B, each added computer costs 1 unit of wheat. '
          'Statement II: As the economy produces more computers, the wheat given up for each extra '
          'computer falls.',
     'opts': ['I is true and II is false',
              'I is true and II is true',
              'I is false and II is true',
              'I is false and II is false'],
     'exp': 'From A to B, 10 more computers cost 10 wheat, so each costs 1 unit and Statement I is '
            'true. Statement II is false: the cost per computer rises from 1 to 3 to 6 wheat, which is '
            'why the curve bows outward.',
     'why': [None,
             'Statement II is false. The wheat given up per computer rises, from 1 to 3 to 6, as '
             'resources better suited to wheat are moved into computers.',
             'Both were misjudged. Statement I is true because A to B trades 10 wheat for 10 '
             'computers, and Statement II is false because the cost per computer rises along the '
             'curve.',
             'Statement I is true: from A to B, wheat falls by 10 while computers rise by 10, so each '
             'added computer costs 1 unit of wheat.'],
     'fig': {'type': 'graph',
             'x': 'Computers',
             'y': 'Wheat (units)',
             'lines': [{'pts': [[10, 85], [35, 77.5], [60, 55], [85, 10]], 'cls': 's', 'label': 'PPC'}],
             'points': [{'at': [10, 85], 'label': 'A'},
                        {'at': [35, 77.5], 'label': 'B'},
                        {'at': [60, 55], 'label': 'C'},
                        {'at': [85, 10], 'label': 'D'}],
             'guides': True,
             'xticks': [[10, '0'], [35, '10'], [60, '20'], [85, '30']],
             'yticks': [[10, '0'], [55, '60'], [77.5, '90'], [85, '100']],
             'alt': 'A bowed-out production possibilities curve for computers on the horizontal axis '
                    'and wheat on the vertical axis. Point A is 0 computers and 100 wheat, point B is '
                    '10 computers and 90 wheat, point C is 20 computers and 60 wheat, and point D is '
                    '30 computers and 0 wheat.'}},
    # id 218
    {'ch': 2,
     'q': "Use the graph. The economy's production possibilities move from PPC1 to PPC2. Which event "
          'could cause this?',
     'opts': ['Contracts and property rights become more reliably enforced',
              'Workers move from producing food into producing clothing',
              'Unemployed workers are hired back by existing factories',
              'Consumers decide they would like more clothing and less food'],
     'exp': 'An improvement in the rules under which the economy functions, such as more reliable '
            'enforcement of contracts and property rights, is one of the four factors that can shift '
            'the PPC outward.',
     'why': [None,
             'Moving workers from food to clothing is a movement along the curve, trading one good for '
             "the other. It doesn't let the economy produce more of both.",
             'Rehiring idle workers moves the economy from inside the curve onto it. The curve itself '
             "doesn't shift.",
             'A change in what consumers want changes which point on the curve is chosen, not how much '
             'the economy is able to produce.'],
     'fig': {'type': 'graph',
             'x': 'Clothing',
             'y': 'Food',
             'lines': [{'pts': [[8, 70], [25, 66], [40, 58], [52, 45], [60, 28], [64, 8]],
                        'cls': 'm',
                        'label': 'PPC1'},
                       {'pts': [[8, 88], [30, 84], [50, 74], [66, 58], [78, 38], [85, 8]],
                        'cls': 's',
                        'label': 'PPC2',
                        'dash': True}],
             'arrows': [{'from': [44, 54], 'to': [56, 66]}],
             'alt': 'Two bowed-out production possibilities curves for food and clothing. PPC1 is '
                    'closer to the origin; PPC2 lies farther out, allowing more of both goods. An '
                    'arrow points from PPC1 toward PPC2.'}},
    # id 219
    {'ch': 2,
     'q': 'Use the graph. Two countries face this same PPC today. Country X chooses point A and '
          'Country Y chooses point B. Other things equal, what is most likely in the future?',
     'opts': ["X's PPC shifts out more than Y's, because X builds more capital now",
              "Y's PPC shifts out more than X's, because Y consumes more goods now",
              'Both PPCs shift out equally, since both start on the same curve',
              "X's PPC shifts inward, because its consumption is lower today"],
     'exp': 'Point A devotes more resources to buildings, equipment, and training. That investment '
            "expands future production possibilities, so X's PPC is likely to shift outward more than "
            "Y's.",
     'why': [None,
             "More consumption today doesn't add to productive capacity. Y invests less, so its PPC is "
             "expected to shift out less than X's.",
             "Starting on the same curve doesn't mean equal growth. How far each curve shifts depends "
             'on how much each country invests now.',
             "Lower consumption today doesn't shrink capacity. X invests more, which tends to shift "
             'its PPC outward, not inward.'],
     'fig': {'type': 'graph',
             'x': 'Consumption goods',
             'y': 'Investment goods',
             'lines': [{'pts': [[8, 85], [30, 80], [50, 70], [66, 55], [78, 35], [84, 8]],
                        'cls': 's',
                        'label': 'PPC'}],
             'points': [{'at': [30, 80], 'label': 'A'}, {'at': [66, 55], 'label': 'B'}],
             'guides': True,
             'xticks': [[30, 'CA'], [66, 'CB']],
             'yticks': [[55, 'IB'], [80, 'IA']],
             'alt': 'A production possibilities curve with consumption goods on the horizontal axis '
                    'and investment goods on the vertical axis. Point A has consumption CA and '
                    'investment IA; point B has more consumption, CB, and less investment, IB.'},
     'expFig': {'type': 'graph',
                'x': 'Consumption goods',
                'y': 'Investment goods',
                'lines': [{'pts': [[84, 8], [78, 35], [66, 55], [50, 70], [30, 80], [8, 85]],
                           'cls': 'm',
                           'label': 'Today'},
                          {'pts': [[8, 89], [32, 84], [53, 74], [70, 58], [82, 37], [88, 8]],
                           'cls': 'd',
                           'label': 'Future, B',
                           'dash': True},
                          {'pts': [[93, 8], [88, 40], [75, 64], [57, 81], [34, 91], [8, 95]],
                           'cls': 's',
                           'label': 'Future, A',
                           'dash': True}],
                'alt': "Today's production possibilities curve, plus two future curves. The future "
                       "curve after choosing high-investment point A lies well outside today's curve; "
                       'the future curve after choosing high-consumption point B lies only slightly '
                       'outside it.'}},
    # id 220
    {'ch': 2,
     'q': 'Use the table. Who has the comparative advantage in producing scarves, and why?',
     'opts': ['Ben, because each scarf costs him 2 loaves while it costs Ana 3',
              'Ana, because she can make more scarves per day than Ben can',
              'Ana, because each scarf costs her 1/3 loaf while it costs Ben 1/2',
              'Ben, because each scarf costs him 1/2 loaf while it costs Ana 1/3'],
     'exp': 'A scarf costs Ana 30 / 10 = 3 loaves and costs Ben 12 / 6 = 2 loaves. Ben is the low '
            'opportunity cost producer of scarves, so he has the comparative advantage in scarves.',
     'why': [None,
             'Making more scarves is absolute advantage. Comparative advantage goes to the lower '
             'opportunity cost: a scarf costs Ana 3 loaves but Ben only 2.',
             'This flips the ratio: 1/3 and 1/2 are scarves given up per loaf, the cost of bread. A '
             'scarf costs Ana 30 / 10 = 3 loaves and Ben 12 / 6 = 2.',
             "The ratios are flipped, and by these numbers Ben's cost would be the higher one. A scarf "
             'actually costs Ben 12 / 6 = 2 loaves and Ana 30 / 10 = 3.'],
     'fig': {'type': 'table',
             'head': ['Producer', 'Bread per day (if only bread)', 'Scarves per day (if only scarves)'],
             'rows': [['Ana', '30', '10'], ['Ben', '12', '6']],
             'alt': 'Each producer can make either good with a full day of work. Ana can make 30 '
                    'loaves of bread or 10 scarves per day. Ben can make 12 loaves of bread or 6 '
                    'scarves per day.'}},
    # id 221
    {'ch': 2,
     'q': 'The table shows the most each person can make in a day if they make only that one good. '
          'Right now Ana makes 15 loaves and 5 scarves a day, and Ben makes 6 loaves and 3 scarves, '
          'for a total of **21 loaves and 8 scarves**. Suppose Ben makes only scarves, and Ana makes '
          'the remaining scarves needed to keep the total at 8, using the rest of her day for bread. '
          'How many more loaves do they make in total?',
     'opts': ['3 more loaves', '6 more loaves', '9 more loaves', '24 more loaves'],
     'exp': 'Ben makes only scarves, so he makes 6 and bakes no bread. Ana then needs only 2 scarves, '
            'which takes 2/10 = 1/5 of her day, leaving 4/5 of her day for bread: 4/5 x 30 = 24 '
            'loaves. Total bread rises from 21 to 24, a gain of 3.',
     'why': [None,
             '6 is the number of loaves Ben stops baking, not the net change. Ana adds 9 loaves (24 - '
             '15) while Ben drops his 6, so the total rises by 3.',
             "9 is Ana's gain alone, 24 - 15. It forgets that Ben no longer bakes his 6 loaves, so the "
             "pair's total rises by only 3.",
             "24 is the pair's new bread total, all baked by Ana, not the change. The question asks "
             'how many more loaves: 24 now minus 21 before is 3.'],
     'fig': {'type': 'table',
             'head': ['Producer', 'Bread per day (if only bread)', 'Scarves per day (if only scarves)'],
             'rows': [['Ana', '30', '10'], ['Ben', '12', '6']],
             'alt': 'Each producer can make either good with a full day of work. Ana can make 30 '
                    'loaves of bread or 10 scarves per day. Ben can make 12 loaves of bread or 6 '
                    'scarves per day.'}},
    # id 222
    {'ch': 2,
     'q': 'One rancher owns her land and may sell it at any time. Another grazes cattle on public land '
          'that anyone may use. Which rancher has the stronger incentive to avoid overgrazing, and '
          'why?',
     'opts': ['The owner, because damage lowers the value of land she can sell later',
              'The public-land rancher, because the costs of the land are widely shared',
              'Both equally, because grass grows back at the same rate on each parcel',
              'The owner, because legal protection lets her ignore the wishes of others'],
     'exp': 'Private owners have a strong incentive to care for and conserve what they own, because '
            'damage lowers the value of property they can sell later. The rancher on open land bears '
            'only a small share of the damage his herd causes.',
     'why': [None,
             'Shared costs weaken the incentive to conserve: each user bears only a small part of the '
             'damage, so overgrazing is more likely on open land.',
             "Regrowth rates don't decide the incentives. The owner captures the land's future value "
             "when she sells; the public-land rancher doesn't.",
             "Ownership doesn't let her ignore others; she bears the opportunity cost of ignoring what "
             "buyers would pay. Her incentive comes from protecting the land's future value."]},
    # id 223
    {'ch': 2,
     'q': 'Statement I: A private owner who ignores what others want bears an opportunity cost, '
          "because she gives up what others would pay for her property's services. Statement II: "
          'Private ownership gives owners an incentive to lower the chance that their property damages '
          "their neighbors' property.",
     'opts': ['I is true and II is true',
              'I is true and II is false',
              'I is false and II is true',
              'I is false and II is false'],
     'exp': 'Both statements describe incentives Gwartney attributes to private property: owners gain '
            "by using resources in ways others value and bear the opportunity cost of ignoring others' "
            "wishes, and they have an incentive to avoid damaging others' property.",
     'why': [None,
             "Statement II is true. Gwartney lists the incentive to lower the chance that one's "
             "property damages others' property as one of the key incentives of private ownership.",
             "Statement I is true. What others would pay for the property's services is a real "
             'opportunity cost, even though no money is paid out when the owner ignores them.',
             "Both are true. Bearing the cost of ignoring others' wishes and the incentive to avoid "
             "damaging neighbors' property are both among private ownership's key incentives."]},
    # id 224
    {'ch': 2,
     'q': 'Selling a used textbook once meant posting flyers and waiting days for a buyer. Now apps '
          'match buyers and sellers within minutes. What is the main economic effect?',
     'opts': ['Lower transaction costs let more mutually beneficial trades happen',
              'The textbooks become more valuable to their original owners',
              'Trades now benefit buyers alone, since sellers face more competition',
              'Fewer trades occur, since the apps are middlemen who raise costs'],
     'exp': 'Apps cut the time and effort of searching out and negotiating trades. Lower transaction '
            "costs mean trades that weren't worth the hassle now happen, creating gains for both "
            'sides.',
     'why': [None,
             "The books' value to their owners doesn't rise; what changes is the cost of trading. "
             'Lower transaction costs let more value-creating trades happen.',
             "Voluntary trades benefit both sides; a seller wouldn't sell unless she expected to gain. "
             'Easier matching helps sellers find buyers too.',
             'This gets middlemen backward: they are valued because they reduce transaction costs, '
             'which leads to more trades, not fewer.']},
    # id 225
    {'ch': 2,
     'q': 'A classmate says, "Grocery stores just add a markup and make nothing. We\'d all be better '
          'off buying straight from farms and dairies." What is wrong with this reasoning?',
     'opts': ['It ignores that grocers cut the time and effort of arranging trades',
              "It's correct, since value comes from production rather than trade",
              "It ignores that grocers set prices so that farmers can't gain from trade",
              "It's correct, since middlemen raise the opportunity cost of shopping"],
     'exp': 'Grocers are middlemen who reduce your transaction costs of getting vegetables from '
            'farmers and milk from dairies. Saving shoppers that time and effort is a real service, so '
            'the markup pays for value created.',
     'why': [None,
             "Value isn't created only by physical production. Trade creates value by moving goods to "
             'people who value them more, and grocers make that cheaper.',
             "Grocers don't block farmers' gains; a farmer sells to a grocer only if the farmer "
             'expects to benefit too.',
             'Middlemen lower the cost of shopping; buying directly from many separate farms and '
             'dairies would take far more time and effort.']},
    # id 226
    {'ch': 2,
     'q': 'Lena owns a concert ticket she values at $40. Marco values the same ticket at $100. Lena '
          'sells it to Marco for $70. How much total value does the trade create?',
     'opts': ['$60, split equally between them',
              '$70, the amount Marco pays Lena',
              "$30, Lena's gain above her value",
              '$0, since no new ticket was made'],
     'exp': 'Lena gains $70 - $40 = $30, and Marco gains $100 - $70 = $30. Moving the ticket to '
            'someone who values it more creates $60 of value in total.',
     'why': [None,
             'The $70 price is a transfer from Marco to Lena, not value created. The value created is '
             "the gap between Marco's $100 value and Lena's $40 value.",
             "$30 counts only Lena's gain. Marco also gains $30 by paying $70 for a ticket he values "
             'at $100.',
             'Trade creates value even without new production, by moving a good from someone who '
             'values it less to someone who values it more.']},
    # id 227
    {'ch': 2,
     'q': 'Tuition stays the same, but a booming job market raises the wages high school graduates can '
          'earn. What does the economic way of thinking predict?',
     'opts': ["College's opportunity cost rises, so fewer people choose to attend",
              "College's cost is unchanged, because tuition has not gone up",
              "College's opportunity cost falls, since jobs make tuition easier to pay",
              "College's cost rises, but enrollment holds steady since value is subjective"],
     'exp': "Forgone earnings are part of college's opportunity cost, so higher wages raise that cost "
            'even with tuition unchanged. When an option becomes more costly, people are less likely '
            'to choose it.',
     'why': [None,
             "Tuition isn't the whole cost. The earnings given up by attending rise with wages, so the "
             'opportunity cost of college rises.',
             'This gets the direction backward. Higher wages mean more earnings are given up to '
             'attend, which raises the cost of college rather than lowering it.',
             "Value is subjective, but when an option's cost rises, people are less likely to choose "
             'it, so enrollment is expected to fall.']},
    # id 228
    {'ch': 2,
     'q': 'Statement I: If people choose to work more and take less leisure, the PPC can shift '
          'outward. Statement II: Putting unemployed workers back to work in existing factories shifts '
          'the PPC outward.',
     'opts': ['I is true and II is false',
              'I is true and II is true',
              'I is false and II is true',
              'I is false and II is false'],
     'exp': "Working harder and giving up leisure is one of Gwartney's four factors that can shift the "
            'PPC outward, so Statement I is true. Statement II is false: idle workers put the economy '
            'inside its curve, and rehiring them moves it onto the existing curve.',
     'why': [None,
             'Statement II is false. Unemployed workers put the economy inside its PPC; putting them '
             'back to work moves output onto the existing curve without shifting it.',
             'Both were misjudged. Giving up leisure to work more can shift the PPC outward, while '
             'rehiring idle workers only moves the economy from inside the curve onto it.',
             'Statement I is true: working harder and giving up current leisure is one of the four '
             'factors that can shift the PPC outward.'],
     'fig': {'type': 'graph',
             'x': 'Clothing',
             'y': 'Food',
             'lines': [{'pts': [[8, 70], [25, 66], [40, 58], [52, 45], [60, 28], [64, 8]],
                        'cls': 's',
                        'label': 'PPC1'}],
             'guides': False,
             'alt': "An economy's starting production possibilities curve, PPC1, bowed out from the "
                    'origin, with food on the vertical axis and clothing on the horizontal axis.'},
     'expFig': {'type': 'graph',
                'x': 'Clothing',
                'y': 'Food',
                'lines': [{'pts': [[8, 70], [25, 66], [40, 58], [52, 45], [60, 28], [64, 8]],
                           'cls': 'm',
                           'label': 'PPC1'},
                          {'pts': [[8, 88], [30, 84], [50, 74], [66, 58], [78, 38], [85, 8]],
                           'cls': 's',
                           'label': 'PPC2',
                           'dash': True}],
                'points': [{'at': [32, 40], 'label': 'U'}, {'at': [40, 58], 'label': 'A'}],
                'arrows': [{'from': [33, 43], 'to': [39, 55]}, {'from': [54, 48], 'to': [64, 56]}],
                'guides': False,
                'alt': 'Point U lies inside the starting curve PPC1, where some workers are '
                       'unemployed. One arrow runs from U up to point A on PPC1, showing idle workers '
                       'being rehired: a move onto the existing curve. A second arrow points from PPC1 '
                       'out to a dashed curve PPC2, showing the outward shift from working more and '
                       'taking less leisure.'}},
    # id 229
    {'ch': 2,
     'q': 'A classmate says, "Country A can produce both cars and wheat using fewer workers than '
          'Country B, so A has nothing to gain from trading with B." What is wrong with this '
          'reasoning?',
     'opts': ['Gains come from differences in opportunity costs, not absolute output',
              "It's correct; trade pays when each country is faster at one of the goods",
              'B would gain from the trade, but A would lose by giving up cheaper goods',
              "A should import both goods from B, since B's workers are paid less"],
     'exp': 'The law of comparative advantage says joint output is greatest when each good is made by '
            'the low opportunity cost producer. Even if A is better at both goods, its opportunity '
            "costs differ from B's, so both gain by specializing and trading.",
     'why': [None,
             'Being faster at a good is absolute advantage. Trade pays when opportunity costs differ, '
             'even if one country is faster at both goods.',
             'Both partners gain from voluntary trade. A specializes where its opportunity cost is '
             'lowest and gets the other good more cheaply through trade.',
             "Money wages don't decide who should produce what. Each good should come from the partner "
             'with the lower opportunity cost.']},
    # id 230
    {'ch': 5,
     'q': 'In the figure, an activity is currently carried out at Q1. From the standpoint of economic '
          'efficiency, what should happen?',
     'opts': ['Expand it toward Q2, since each added unit up to Q2 is worth more than it costs',
              'Keep it at Q1, since total cost there is lower than at any larger quantity',
              'Cut it back, since the marginal cost curve is already rising at Q1',
              'Expand it past Q2 to Q3, where the total benefit from the activity is greatest'],
     'exp': 'At Q1 the MB curve lies above the MC curve, so each additional unit up to Q2 adds more '
            'benefit than cost. Expanding to Q2, where MB equals MC, raises net gains.',
     'why': [None,
             'Lower total cost is not the goal. At Q1, units worth more than they cost are left '
             'undone, so staying there gives up net gains.',
             "A rising MC curve doesn't matter by itself; what matters is MB compared with MC. At Q1, "
             'MB is still above MC, so the activity should grow, not shrink.',
             'Total benefit may keep rising past Q2, but every unit beyond Q2 has a marginal cost '
             'above its marginal benefit, so net gains fall.'],
     'fig': {'type': 'graph',
             'x': 'Quantity of the activity',
             'y': 'Dollars per unit',
             'lines': [{'pts': [[10, 85], [90, 15]], 'cls': 'g', 'label': 'MB'},
                       {'pts': [[10, 15], [90, 85]], 'cls': 's', 'label': 'MC'}],
             'points': [{'at': [50, 50], 'label': 'A'}],
             'guides': True,
             'xticks': [[30, 'Q1'], [50, 'Q2'], [70, 'Q3']],
             'alt': 'A downward-sloping marginal benefit curve MB and an upward-sloping marginal cost '
                    'curve MC cross at point A, above quantity Q2. Quantity Q1 lies to the left of Q2 '
                    'and quantity Q3 lies to the right of Q2.'}},
    # id 231
    {'ch': 5,
     'q': 'Use the figure. Statement I: Total benefit from the activity is greater at Q3 than at Q2. '
          'Statement II: Moving from Q2 to Q3 makes the use of resources more efficient.',
     'opts': ['Statement I is true and Statement II is false',
              'Both Statement I and Statement II are true',
              'Statement I is false and Statement II is true',
              'Both Statement I and Statement II are false'],
     'exp': 'Between Q2 and Q3 marginal benefit is still positive, so total benefit keeps rising and '
            'Statement I is true. But each of those units costs more than it adds, so net gains fall '
            'and Statement II is false.',
     'why': [None,
             'Statement II is false. From Q2 to Q3, MC lies above MB, so each added unit is worth less '
             'than it costs; more total benefit is not the same as more efficiency.',
             'Both judgments are reversed. Total benefit rises from Q2 to Q3 because MB stays above '
             'zero, while efficiency falls because MC exceeds MB there.',
             'Statement I is true: MB is still above zero between Q2 and Q3, so each unit adds some '
             'benefit and total benefit is larger at Q3.'],
     'fig': {'type': 'graph',
             'x': 'Quantity of the activity',
             'y': 'Dollars per unit',
             'lines': [{'pts': [[10, 85], [90, 15]], 'cls': 'g', 'label': 'MB'},
                       {'pts': [[10, 15], [90, 85]], 'cls': 's', 'label': 'MC'}],
             'points': [{'at': [50, 50], 'label': 'A'}],
             'guides': True,
             'xticks': [[30, 'Q1'], [50, 'Q2'], [70, 'Q3']],
             'alt': 'A downward-sloping marginal benefit curve MB and an upward-sloping marginal cost '
                    'curve MC cross at point A, above quantity Q2. Quantity Q1 lies to the left of Q2 '
                    'and quantity Q3 lies to the right of Q2.'}},
    # id 232
    {'ch': 5,
     'q': "A paper mill's emissions damage downstream fisheries. In the figure, S1 reflects only the "
          "mill's own costs, while S2 adds the harm to the fisheries. Where will the market settle?",
     'opts': ['At Q1 and P1, with more output and a lower price than full costs would imply',
              'At Q2 and P2, because buyers end up paying for the damage through price',
              'At Q1 and P2, because the damage raises price without changing output',
              "At Q2 and P1, because the harm cuts output but leaves buyers' price unchanged"],
     'exp': "The mill doesn't bear the harm it causes, so S1 understates the true cost of production "
            'and the market settles at E1, output Q1 and price P1. That is more output and a lower '
            'price than at E2, where all costs are counted.',
     'why': [None,
             'E2 is the outcome only if the external cost were registered in the market. Because the '
             "mill ignores the fisheries' harm, the market follows S1, not S2.",
             "Q1 and P2 don't occur together on any curve here. Unregistered damage doesn't raise the "
             'price at all; the market follows S1 to price P1.',
             'This mixes the two equilibria. If the harm were counted, both output and price would '
             "change, to Q2 and P2; since it isn't, neither changes."],
     'fig': {'type': 'graph',
             'x': 'Quantity',
             'y': 'Price',
             'lines': [{'pts': [[10, 85], [90, 15]], 'cls': 'd', 'label': 'D'},
                       {'pts': [[10, 15], [90, 85]], 'cls': 's', 'label': 'S1'},
                       {'pts': [[10, 43], [66, 92]], 'cls': 's', 'label': 'S2', 'dash': True}],
             'points': [{'at': [50, 50], 'label': 'E1'}, {'at': [34, 64], 'label': 'E2'}],
             'guides': True,
             'xticks': [[34, 'Q2'], [50, 'Q1']],
             'yticks': [[50, 'P1'], [64, 'P2']],
             'alt': 'A downward-sloping demand curve D crosses supply curve S1 at E1, at quantity Q1 '
                    'and price P1. A second supply curve S2 lies above and to the left of S1 and '
                    'crosses D at E2, at the smaller quantity Q2 and the higher price P2.'}},
    # id 233
    {'ch': 5,
     'q': 'A drug company develops a flu vaccine, and each shot also protects people who never get '
          "one. In the figure, D1 reflects buyers' own benefits and D2 includes all benefits. How does "
          'the market outcome compare with the efficient one?',
     'opts': ['It settles at Q1, short of the efficient Q2, at a price below P2',
              'It settles at Q2, since buyers count the protection given to others',
              'It settles at Q1, beyond the efficient level because P1 is too low',
              "It settles at Q2, but at P1 because the extra benefit isn't priced"],
     'exp': 'Buyers weigh only their own benefits, so market demand is D1 and the market settles at Q1 '
            'and P1. Counting the protection given to nonbuyers gives D2, with the larger output Q2 '
            'and higher price P2, so too few units are produced.',
     'why': [None,
             "Buyers don't count benefits that go to others; that is what makes them external. Market "
             'demand is D1, not D2, so output stops at Q1.',
             "A low price doesn't signal overproduction here. Q1 is less than the efficient Q2, "
             "because demand understates the vaccine's total value.",
             "Q2 and P1 don't occur together. Output reaches Q2 only if demand were D2, and that "
             'higher demand would also raise the price to P2.'],
     'fig': {'type': 'graph',
             'x': 'Quantity',
             'y': 'Price',
             'lines': [{'pts': [[10, 15], [90, 85]], 'cls': 's', 'label': 'S'},
                       {'pts': [[10, 71], [78, 11.5]], 'cls': 'd', 'label': 'D1'},
                       {'pts': [[10, 92], [90, 22]], 'cls': 'd', 'label': 'D2', 'dash': True}],
             'points': [{'at': [42, 43], 'label': 'E1'}, {'at': [54, 53.5], 'label': 'E2'}],
             'guides': True,
             'xticks': [[42, 'Q1'], [54, 'Q2']],
             'yticks': [[43, 'P1'], [53.5, 'P2']],
             'alt': 'An upward-sloping supply curve S crosses demand curve D1 at E1, at quantity Q1 '
                    'and price P1. A second demand curve D2 lies to the right of D1 and crosses S at '
                    'E2, at the larger quantity Q2 and the higher price P2.'}},
    # id 234
    {'ch': 5,
     'q': 'Sellers in a market form an association that limits entry, and supply shifts from S1 to S2 '
          'in the figure. Compared with the competitive outcome, what happens?',
     'opts': ['Output falls to Q2 and price rises to P2, so too few units are produced',
              'Output falls to Q2 and price rises to P2; this corrects overproduction at Q1',
              'Price rises to P2, but output stays at Q1 because demand has not changed',
              'Demand falls along with supply, so output drops but price stays at P1'],
     'exp': 'Restricting entry shifts supply to S2, moving the market from E1 to E2: output falls to '
            'Q2 and price rises to P2. The competitive output Q1 was efficient, so too few units are '
            'now produced.',
     'why': [None,
             "Nothing was overproduced at Q1; the competitive supply reflected sellers' true costs. "
             'Units between Q2 and Q1 were worth more to buyers than they cost, so cutting them is a '
             'loss.',
             'With demand unchanged, a leftward supply shift moves the market up along D, so quantity '
             "demanded falls as price rises. Output can't stay at Q1.",
             'Restricting entry shifts supply, not demand. With demand unchanged, the smaller supply '
             'raises the price to P2 rather than leaving it at P1.'],
     'fig': {'type': 'graph',
             'x': 'Quantity',
             'y': 'Price',
             'lines': [{'pts': [[10, 85], [90, 15]], 'cls': 'd', 'label': 'D'},
                       {'pts': [[10, 15], [90, 85]], 'cls': 's', 'label': 'S1'},
                       {'pts': [[10, 43], [66, 92]], 'cls': 's', 'label': 'S2', 'dash': True}],
             'points': [{'at': [50, 50], 'label': 'E1'}, {'at': [34, 64], 'label': 'E2'}],
             'guides': True,
             'xticks': [[34, 'Q2'], [50, 'Q1']],
             'yticks': [[50, 'P1'], [64, 'P2']],
             'alt': 'A downward-sloping demand curve D crosses supply curve S1 at E1, at quantity Q1 '
                    'and price P1. A second supply curve S2 lies to the left of S1 and crosses D at '
                    'E2, at the smaller quantity Q2 and the higher price P2.'}},
    # id 235
    {'ch': 5,
     'q': 'Two markets each see supply shift left from S1 to S2: in market X because sellers restrict '
          'entry, and in market Y because a previously ignored pollution cost is now counted. Which '
          'statement about efficiency is correct?',
     'opts': ['In X the original Q1 was efficient; in Y the smaller Q2 is the efficient level',
              'In both, the smaller Q2 is efficient since higher prices cut wasteful use',
              'In X the smaller Q2 is efficient; in Y the original Q1 was the efficient level',
              'In both, the original Q1 was efficient since it came from voluntary trade'],
     'exp': "In X, S1 reflected sellers' true costs, so the competitive Q1 was efficient and the "
            'cutback means too few units. In Y, S2 adds the ignored pollution cost, so it shows the '
            'true cost of production and Q2 is efficient; Q1 was too many.',
     'why': [None,
             'Right for Y but not for X. When sellers restrict entry, S1 already reflected true costs, '
             'so cutting to Q2 loses units worth more to buyers than they cost.',
             'This reverses the two cases. Counting an ignored cost corrects supply in Y, while '
             'restricting entry distorts supply in X.',
             'Right for X but not for Y. Voluntary trade in Y ignored the pollution borne by others, '
             'so Q1 included units valued less than their full cost.'],
     'fig': {'type': 'graph',
             'x': 'Quantity',
             'y': 'Price',
             'lines': [{'pts': [[10, 85], [90, 15]], 'cls': 'd', 'label': 'D'},
                       {'pts': [[10, 15], [90, 85]], 'cls': 's', 'label': 'S1'},
                       {'pts': [[10, 43], [66, 92]], 'cls': 's', 'label': 'S2', 'dash': True}],
             'points': [{'at': [50, 50], 'label': 'E1'}, {'at': [34, 64], 'label': 'E2'}],
             'guides': True,
             'xticks': [[34, 'Q2'], [50, 'Q1']],
             'yticks': [[50, 'P1'], [64, 'P2']],
             'arrows': [{'from': [78, 78], 'to': [55, 78]}],
             'alt': 'A downward-sloping demand curve D crosses supply curve S1 at E1, at quantity Q1 '
                    'and price P1. An arrow points left from S1 to a dashed supply curve S2, which '
                    'crosses D at E2, at the smaller quantity Q2 and the higher price P2. The same '
                    'graph applies to both markets.'}},
    # id 236
    {'ch': 5,
     'q': 'A town asks residents to chip in voluntarily for mosquito spraying that will cover every '
          'neighborhood. Many residents decline, and too little money is raised. What best explains '
          'this?',
     'opts': ["Nonpayers can't be kept from the benefit, so many let others pay",
              "Spraying is rival, so each payer's benefit shrinks as more join in",
              'The single spraying company lacks competition and charges too much',
              'Residents lack information about whether spraying actually works'],
     'exp': 'Mosquito spraying is a public good: once provided, it protects everyone, and nonpayers '
            "can't be excluded. Each resident therefore has an incentive to free ride, and too little "
            'money is raised.',
     'why': [None,
             "Spraying is nonrival: one household's protection doesn't reduce another's. The shortfall "
             "comes from the fact that nonpayers can't be excluded, not from rivalry.",
             "The problem appears before any price is set: residents won't contribute voluntarily. A "
             "single seller's pricing doesn't explain refusing to pay for a benefit you get anyway.",
             "Even residents sure that spraying works have reason to let others pay, since they can't "
             "be excluded. Doubt about effectiveness isn't the core problem."]},
    # id 237
    {'ch': 5,
     'q': 'A classmate argues: "National defense is a public good because government provides it. City '
          'buses are run by government too, so bus rides are a public good." What is wrong with this '
          'reasoning?',
     'opts': ['Bus seats are rival and nonpayers can be excluded, whatever the sector',
              'Government cannot supply a public good, so neither example qualifies',
              'Defense is excludable, so it does not qualify as a public good either',
              'Bus rides become public goods once they are given away free of charge to riders'],
     'exp': 'Whether a good is public depends on its characteristics, nonrival and nonexcludable, not '
            "on who produces it. A seat taken by one rider isn't available to another, and fares can "
            'keep nonpayers off.',
     'why': [None,
             'Government can and does supply public goods, such as national defense. The flaw is using '
             "the producer, rather than the good's characteristics, as the test.",
             'National defense is a standard public good: it protects everyone in the country at once, '
             "and nonpayers can't be left out.",
             "Price doesn't decide it. A free bus seat is still rival, since one rider's use takes it "
             'from others, and nonpayers could still be excluded.']},
    # id 238
    {'ch': 5,
     'q': 'In which purchase is the buyer most likely to face a serious information problem?',
     'opts': ['Hiring a roofer for a job done once every 20 years',
              'Buying a latte at the same cafe every weekday',
              'Filling the car up at the station on your commute',
              'Picking up a favorite cereal during weekly shopping'],
     'exp': 'Information problems are serious when a good is hard to evaluate on inspection and seldom '
            "bought repeatedly from the same seller. A roofer is hired rarely, and the job's quality "
            'may not show for years.',
     'why': [None,
             'A daily latte from the same cafe is a repeat purchase: the buyer learns from experience, '
             'and the cafe wants her to come back.',
             'Regular fill-ups at a station on the commute are repeat purchases, so the buyer quickly '
             'learns whether the station is reliable.',
             'A favorite cereal bought every week is a repeat purchase whose quality the buyer already '
             'knows, so the information problem is minimal.']},
    # id 239
    {'ch': 5,
     'q': 'A traveler in an unfamiliar city chooses a nationally franchised hotel over a local inn she '
          'knows nothing about. How does the chapter explain this choice?',
     'opts': ['The brand offers standardized quality to a buyer unlikely to return',
              'The franchise is a public good that every traveler can use at once',
              "The local inn's lack of competition lets it charge too much to stay",
              "Hotel stays are repeat purchases, so she already knows the inn's quality"],
     'exp': "When buyers can't rely on repeat dealings, brand names and franchises supply information "
            "by promising standardized quality and dependability. Firms profit by solving the buyer's "
            'information problem.',
     'why': [None,
             "A hotel room is rival, and nonpayers are excluded, so it isn't a public good. The "
             "franchise's appeal is the information its brand provides.",
             "Nothing suggests the inn faces no rivals or overcharges. She avoids it because she can't "
             'judge its quality, which is an information problem.',
             'A traveler passing through rarely buys repeatedly from the same local inn, and she knows '
             "nothing about this one, so she can't rely on experience. That is exactly why she turns "
             'to the brand.']},
    # id 240
    {'ch': 5,
     'q': "Used-car buyers often can't tell whether a transmission is about to fail, and most rarely "
          'buy twice from the same dealer. Which reason the invisible hand may fail does this '
          'illustrate?',
     'opts': ['Poor information', 'External costs', 'Lack of competition', 'Public goods'],
     'exp': 'The car is hard to evaluate on inspection, and buyers seldom buy repeatedly from the same '
            'dealer. These are the conditions the text gives for an information problem.',
     'why': [None,
             'External costs fall on people outside a transaction without their consent. A hidden '
             'defect harms the buyer, who chose to trade.',
             'Lack of competition means sellers restrict output and raise prices. The problem here is '
             "that buyers can't judge quality, not that dealers are few.",
             "A used car is rival and excludable, so it isn't a public good. The issue is what the "
             'buyer can know before buying.']},
    # id 241
    {'ch': 5,
     'q': "Which of the following is an example of government's **protective** function?",
     'opts': ['A court ruling on a broken contract between two firms',
              'A central bank keeping the money supply stable over time',
              'A county spraying for mosquitoes in every neighborhood',
              'A state building roads that private firms would not build'],
     'exp': 'The protective function includes a legal structure that enforces contracts and settles '
            'disputes, so a court ruling on a broken contract is protective.',
     'why': [None,
             'This chapter lists a stable monetary and financial environment under the productive '
             'function, among the goods that are hard to supply through markets.',
             'Mosquito abatement is a public good that government produces, so it falls under the '
             'productive function, not protection of people and property.',
             'Supplying goods that private markets provide poorly is the productive function. '
             'Protection concerns people, property, and enforcing the rules.']},
    # id 242
    {'ch': 5,
     'q': 'A council member proposes spending whatever it takes to repair every pothole in the city '
          "within 24 hours of being reported. What is the economist's main objection?",
     'opts': ['Past some point, the added cost of faster repair exceeds its added benefit',
              'Road repair is a public good, so private markets should handle it instead',
              'Potholes are an external cost, so the drivers who cause them should pay',
              'Repairs create external benefits, so the city should spend even more'],
     'exp': 'Even worthy activities can be pursued beyond the efficient level. At some point the extra '
            'benefit of faster or more complete repair is less than its extra cost, so spending '
            'whatever it takes is inefficient.',
     'why': [None,
             'Public goods are hard for markets to supply, which argues for government provision, not '
             'against it. The objection is to the cost-blind goal, not to who provides roads.',
             "This shifts the debate to who should pay. The economist's objection is that the goal "
             'ignores cost, whoever ends up paying it.',
             'Even with spillover benefits, the rule is to expand only while marginal benefit exceeds '
             'marginal cost. That never justifies spending whatever it takes.']},
    # id 243
    {'ch': 5,
     'q': 'A classmate says, "Market failure means some firms in a market are losing money." What is '
          'the problem with this definition?',
     'opts': ['Market failure means markets fall short of ideal economic efficiency',
              'Market failure means a market has more sellers than demand supports',
              "Market failure means a market's prices have risen faster than wages",
              'Market failure means government has stepped in to set market prices'],
     'exp': 'Market failure means markets fall short of ideal economic efficiency, usually traced to '
            'lack of competition, externalities, public goods, or poor information. Losses for some '
            'firms are a normal part of a working market.',
     'why': [None,
             'Too many sellers for the demand leads to losses and exit, which is how markets move '
             'resources to better uses. That is not what market failure means.',
             'Comparing price growth with wage growth concerns living standards, not efficiency. '
             'Market failure is about whether resources are used efficiently.',
             'Government action is a possible response to market failure, not its definition. Markets '
             'can fail with no government involvement at all.']},
    # id 244
    {'ch': 5,
     'q': 'Car exhaust in a metro area of several million people creates smog. According to the '
          'chapter, what is likely to be the most practical response?',
     'opts': ['Requiring cars to carry devices that limit their emissions',
              'Defining property rights so each resident can sue each driver',
              'Leaving it alone, since drivers already pay for gas and cars',
              "Banning cars until the area's air is perfectly clean again"],
     'exp': "Defining and enforcing property rights isn't realistic when millions of people are "
            'involved, so regulations requiring devices that limit emissions may be the best option.',
     'why': [None,
             'Property rights address the root cause, but with millions of drivers and residents, '
             'individual lawsuits are impractical, as the chapter notes for large-number cases.',
             "Paying for gas and cars covers drivers' own costs, not the harm smog does to others. The "
             'external cost stays unregistered in the market.',
             "This ignores trade-offs. Perfectly clean air isn't worth any cost, and banning cars "
             'would give up benefits far larger than the last bits of pollution removed.']},
    # id 245
    {'ch': 6,
     'q': "A town votes on a park-and-trail project costing $35. The table shows each voter's benefit "
          'and tax under two plans. Under Plan A, how does the majority vote turn out, and is the '
          'project efficient?',
     'opts': ['It fails 2 to 3, even though total benefits exceed the cost by $15',
              'It passes 3 to 2, since Baker, Cruz, and Ford all gain from it',
              'It fails 2 to 3, which is efficient since most voters would lose',
              'It passes 5 to 0, since total benefits are larger than the total tax'],
     'exp': 'Under Plan A each voter pays $7, so only Baker, with $24 in benefits, and Cruz, with $15, '
            'gain; Ford, Hill, and Ito vote no and the project fails 2 to 3. Yet total benefits of $50 '
            'exceed the $35 cost by $15, so it is efficient.',
     'why': [None,
             "Ford's $6 benefit is less than his $7 tax, so he loses $1 and votes no. Only Baker and "
             'Cruz gain under Plan A.',
             'Efficiency compares total benefits with total costs, not how many voters gain. Benefits '
             'of $50 exceed the $35 cost, so the project is efficient even though it fails.',
             'Each voter compares their own benefit with their own $7 tax, not the totals. Ford, Hill, '
             'and Ito would lose, so they vote no.'],
     'fig': {'type': 'table',
             'head': ['Voter', 'Benefit received', 'Tax under Plan A', 'Tax under Plan B'],
             'rows': [['Baker', '$24', '$7.00', '$16.80'],
                      ['Cruz', '$15', '$7.00', '$10.50'],
                      ['Ford', '$6', '$7.00', '$4.20'],
                      ['Hill', '$3', '$7.00', '$2.10'],
                      ['Ito', '$2', '$7.00', '$1.40'],
                      ['Total', '$50', '$35.00', '$35.00']],
             'alt': 'A table of five voters with the benefit each receives from a proposed '
                    'park-and-trail project and the tax each would pay under two plans. Baker: benefit '
                    '$24, Plan A $7.00, Plan B $16.80. Cruz: $15, $7.00, $10.50. Ford: $6, $7.00, '
                    '$4.20. Hill: $3, $7.00, $2.10. Ito: $2, $7.00, $1.40. Totals: benefit $50, Plan A '
                    '$35.00, Plan B $35.00.'}},
    # id 246
    {'ch': 6,
     'q': "Using the table, suppose the town adopts Plan B instead, so each voter's tax is in "
          "proportion to benefits. What is the vote, and what is Ford's net gain?",
     'opts': ['It passes 5 to 0, and Ford gains $1.80',
              'It passes 5 to 0, and Ford gains $6.00',
              'It passes 3 to 2, and Ford loses $1.00',
              'It fails 2 to 3, and Ford gains $1.80'],
     'exp': 'Under Plan B each voter pays 70 percent of their benefit, since $35 / $50 = 0.7, so '
            "everyone gains and the project passes 5 to 0. Ford's net gain is $6.00 - $4.20 = $1.80.",
     'why': [None,
             "This forgets to subtract Ford's $4.20 tax. $6.00 is his gross benefit, not his net gain.",
             "This uses Plan A's $7 tax. Under Plan B Ford pays only $4.20, so he gains and votes yes, "
             'along with everyone else.',
             "The 2-to-3 defeat is the Plan A result. Under Plan B every voter's benefit exceeds their "
             'tax, so all five vote yes.'],
     'fig': {'type': 'table',
             'head': ['Voter', 'Benefit received', 'Tax under Plan A', 'Tax under Plan B'],
             'rows': [['Baker', '$24', '$7.00', '$16.80'],
                      ['Cruz', '$15', '$7.00', '$10.50'],
                      ['Ford', '$6', '$7.00', '$4.20'],
                      ['Hill', '$3', '$7.00', '$2.10'],
                      ['Ito', '$2', '$7.00', '$1.40'],
                      ['Total', '$50', '$35.00', '$35.00']],
             'alt': 'A table of five voters with the benefit each receives from a proposed '
                    'park-and-trail project and the tax each would pay under two plans. Baker: benefit '
                    '$24, Plan A $7.00, Plan B $16.80. Cruz: $15, $7.00, $10.50. Ford: $6, $7.00, '
                    '$4.20. Hill: $3, $7.00, $2.10. Ito: $2, $7.00, $1.40. Totals: benefit $50, Plan A '
                    '$35.00, Plan B $35.00.'}},
    # id 247
    {'ch': 6,
     'q': 'One bill combines three projects; the table shows the net benefit or cost of each project '
          'to voters in each of five equal-sized districts. What happens if each project is voted on '
          'separately, versus as one bill?',
     'opts': ['Each fails 1 to 4 alone, but the bill passes 3 to 2 at a net loss of $10',
              'Each fails 1 to 4 alone, and the bill fails too since its total is -$10',
              'Each passes alone, and the bill passes 3 to 2 at a net gain of $12',
              'Each fails 1 to 4 alone, but the bill passes 3 to 2 at a net gain of $12'],
     'exp': 'Separately, only the host district gains from each project, so each fails 1 to 4. '
            'Bundled, A, B, and C net +$7, +$3, and +$2, while D and E each net -$11, so the bill '
            'passes 3 to 2 though the total is 7 + 3 + 2 - 11 - 11 = -$10.',
     'why': [None,
             "Districts don't vote on the bill's overall total; each votes on its own net gain. A, B, "
             'and C all come out ahead, so they pass it 3 to 2.',
             'Each project helps only its host district and costs the other four, so alone each fails '
             "1 to 4. The $12 also adds only the winners' gains.",
             "The vote counts are right, but $12 adds only A, B, and C's gains and ignores the $22 "
             'lost by D and E, leaving a net loss of $10.'],
     'fig': {'type': 'table',
             'head': ['Voters of district', 'Bridge in A', 'Park in B', 'Lab in C'],
             'rows': [['A', '+$14', '-$3', '-$4'],
                      ['B', '-$4', '+$11', '-$4'],
                      ['C', '-$4', '-$3', '+$9'],
                      ['D', '-$4', '-$3', '-$4'],
                      ['E', '-$4', '-$3', '-$4']],
             'alt': 'Net benefit or cost to the voters of districts A through E from three projects in '
                    'one bill. District A: bridge +$14, park -$3, lab -$4. District B: bridge -$4, '
                    'park +$11, lab -$4. District C: bridge -$4, park -$3, lab +$9. District D: bridge '
                    '-$4, park -$3, lab -$4. District E: bridge -$4, park -$3, lab -$4.'}},
    # id 248
    {'ch': 6,
     'q': 'A bill would give a large subsidy to about 300 specialty-cheese makers, paid for by a tiny '
          'charge added to every grocery bill nationwide. Using the table, which type is this, and how '
          'is the political process likely to treat it?',
     'opts': ['Type 2; likely to pass even if it is counterproductive',
              'Type 4; likely to be rejected even if it is productive',
              'Type 2; likely to pass when productive and fail when not',
              'Type 1; likely to pass when productive and fail when not'],
     'exp': 'Benefits go to a small group while costs are spread thinly over many grocery shoppers, '
            'which is Type 2. Representative government is biased toward adopting such projects, even '
            'when they are counterproductive.',
     'why': [None,
             'Type 4 is the reverse pattern, widespread benefits with concentrated costs. Here the '
             'benefits go to about 300 producers, so they are concentrated.',
             "The type is right but the outcome isn't. In Type 2 the motivated few push hard while the "
             'many barely notice, so even inefficient projects tend to pass.',
             'Type 1 has both benefits and costs widespread. Here the benefits go to only about 300 '
             'cheese makers, so they are concentrated.'],
     'fig': {'type': 'table',
             'head': ['Type', 'Distribution of benefits', 'Distribution of costs'],
             'rows': [['1', 'Widespread', 'Widespread'],
                      ['2', 'Concentrated', 'Widespread'],
                      ['3', 'Concentrated', 'Concentrated'],
                      ['4', 'Widespread', 'Concentrated']],
             'alt': 'The four ways benefits and costs can be distributed among voters. Type 1: '
                    'benefits widespread, costs widespread. Type 2: benefits concentrated, costs '
                    'widespread. Type 3: benefits concentrated, costs concentrated. Type 4: benefits '
                    'widespread, costs concentrated.'}},
    # id 249
    {'ch': 6,
     'q': "A rule would cut air pollution for a whole state's residents, with all the costs paid by "
          'three cement plants. Using the table, how is the political process likely to handle it?',
     'opts': ['It will likely reject the rule even if it is productive',
              'It will likely adopt it even if it is unproductive',
              'It tends to adopt it if productive, reject if not',
              'It will likely adopt it, since far more voters gain than lose'],
     'exp': 'Widespread benefits with concentrated costs is Type 4. The three plants bearing the cost '
            'fight hard, while residents who each gain a little pay little attention, so even '
            'productive projects are often rejected.',
     'why': [None,
             'A bias toward adoption applies to Type 2, concentrated benefits with widespread costs. '
             'Here the concentration is on the cost side.',
             'Voting tends to sort projects well only when benefits and costs are both widespread or '
             'both concentrated. This case mismatches them.',
             "Headcount isn't decisive. Rationally ignorant residents who each gain a little exert "
             'little pressure, while the few heavily affected plants are well organized.'],
     'fig': {'type': 'table',
             'head': ['Type', 'Distribution of benefits', 'Distribution of costs'],
             'rows': [['1', 'Widespread', 'Widespread'],
                      ['2', 'Concentrated', 'Widespread'],
                      ['3', 'Concentrated', 'Concentrated'],
                      ['4', 'Widespread', 'Concentrated']],
             'alt': 'The four ways benefits and costs can be distributed among voters. Type 1: '
                    'benefits widespread, costs widespread. Type 2: benefits concentrated, costs '
                    'widespread. Type 3: benefits concentrated, costs concentrated. Type 4: benefits '
                    'widespread, costs concentrated.'}},
    # id 250
    {'ch': 6,
     'q': 'Dana votes in every election but has no idea where the candidates stand on federal farm '
          'policy. How would public choice analysis describe her behavior?',
     'opts': ['Studying farm policy costs her more than she gains, since her vote rarely decides',
              'She is irrational, because better information would reliably pay off for her',
              "She is showing the shortsightedness effect by ignoring farm policy's future costs",
              'She is a member of a special interest group that benefits from staying quiet'],
     'exp': 'This is the rational ignorance effect: becoming informed costs time and effort, and one '
            'vote is unlikely to be decisive, so staying uninformed on many issues is a sensible '
            'choice.',
     'why': [None,
             'Public choice treats her choice as rational. Because her vote is very unlikely to change '
             'the outcome, the payoff to studying farm policy is small.',
             'Shortsightedness concerns policies with clear current benefits and hidden future costs. '
             'Her lack of information reflects the cost of learning, not a focus on the present.',
             'Special interest members are usually well informed about their issue, since it affects '
             'them heavily. Dana knows nothing about it, which fits rational ignorance.']},
    # id 251
    {'ch': 6,
     'q': 'Statement I: The U.S. sugar program persists partly because each grower gains a lot and is '
          "politically active, while each household's cost is small. Statement II: The program "
          'persists because its total benefits to growers exceed its total costs to consumers.',
     'opts': ['Statement I is true and Statement II is false',
              'Both Statement I and Statement II are true',
              'Statement I is false and Statement II is true',
              'Both Statement I and Statement II are false'],
     'exp': 'Statement I describes the special interest effect: each grower gains a lot and is '
            "politically active, while each household's small cost leaves consumers uninformed. "
            'Statement II is false: the program continues even though it is counterproductive.',
     'why': [None,
             'Statement II is false. The sugar program is counterproductive, so its costs exceed its '
             'benefits; it survives because of political incentives, not efficiency.',
             'Both judgments are reversed. Statement I is the special interest effect that explains '
             'persistence; Statement II wrongly assumes a lasting program must be efficient.',
             'Statement I is true: large gains to each grower and small costs to each household is the '
             'special interest effect the text uses to explain the program.']},
    # id 252
    {'ch': 6,
     'q': "A state legislature cuts this year's income tax for every resident and covers the lost "
          'revenue by borrowing that must be repaid over the next 30 years. Which concept best '
          'explains why this is politically attractive?',
     'opts': ['The shortsightedness effect',
              'The rational ignorance effect',
              'The bundle-purchase problem',
              'The special interest effect'],
     'exp': 'Voters see the tax cut now, while repayment falls in the future and is hard to identify. '
            'That is the shortsightedness effect, which makes debt financing politically attractive.',
     'why': [None,
             'Rational ignorance may keep voters from noticing the debt, but the defining feature here '
             'is a current benefit paid for with future costs.',
             "The bundle-purchase problem concerns voters having to accept a candidate's whole package "
             "of positions. It doesn't explain trading current benefits for future costs.",
             'The special interest effect requires concentrated benefits. Here every resident gets the '
             'tax cut, so the benefits are widespread.']},
    # id 253
    {'ch': 6,
     'q': 'Which of the following is the best example of rent seeking?',
     'opts': ['A trade group lobbying for a tariff that shields its members from imports',
              'A firm cutting its prices to win over the customers of a nearby competitor',
              'A startup spending heavily on research to build a longer-lasting battery',
              'A retailer advertising heavily to draw shoppers away from rival stores'],
     'exp': 'Rent seeking uses the political process to restructure policy so income is redirected '
            'toward oneself. A protective tariff transfers income from consumers to the industry.',
     'why': [None,
             'Cutting prices to win customers is market competition, which benefits consumers. It '
             "doesn't use government to redirect income.",
             'Research creates new value through the market. Rent seeking diverts resources away from '
             'productive activity toward obtaining favors.',
             'Advertising competes for customers in the market, not through policy. Rent seeking '
             'requires seeking a favor from government.']},
    # id 254
    {'ch': 6,
     'q': 'Officials in a federal agriculture agency and a large farm lobby both push to expand a '
          'crop-support program. Why are their goals often aligned?',
     'opts': ["A bigger program serves the officials' career goals and the group's income",
              "Officials are elected by farm voters and must follow the farm group's wishes",
              'The program is a public good, so both sides gain from its free riders',
              "The program's costs fall mainly on farmers, so taxpayers are unaffected"],
     'exp': 'Bureaucrats seek promotion, job security, and power, and larger budgets serve those '
            'goals, so their interests are often complementary with those of the interest groups they '
            'serve.',
     'why': [None,
             'Bureaucrats are civil servants, not elected officials. Their link to the farm group '
             'comes from a shared interest in program growth, not from votes.',
             "A crop-support program benefits a specific group, and nonrecipients don't get the "
             "payments, so it isn't a public good. Free riding doesn't explain the alliance.",
             'Taxpayers and consumers bear the costs of crop supports. Farmers are the ones receiving '
             'the benefits, not paying for them.']},
    # id 255
    {'ch': 6,
     'q': "A city-run bus garage and a private trucking firm's garage each find a way to cut "
          'maintenance costs by 10 percent. Why is the city manager less likely to push the change '
          'through?',
     'opts': ["She rarely gains personally from savings and spends other people's money",
              'Public garages have more competition, so their costs are already low',
              'Voters closely track garage costs, so any change draws heavy scrutiny',
              'City managers lack the information needed to measure any cost savings'],
     'exp': "Public-sector managers seldom gain personally from cost cuts and spend other people's "
            'money, and there is no profit motive or bankruptcy process to push efficiency. So the '
            'incentive to adopt the savings is weak.',
     'why': [None,
             'Public agencies lack the profit motive and bankruptcy process that pressure private '
             'firms, which weakens rather than strengthens the push to keep costs low.',
             'Rationally ignorant voters pay little attention to details like garage costs. Weak '
             'incentives, not heavy scrutiny, hold the change back.',
             "Both garages found the same savings, so information isn't the issue. The difference is "
             'that the city manager has little to gain personally.']},
    # id 256
    {'ch': 6,
     'q': 'Firm X earns profits by making solar panels that cost less to produce than buyers value '
          'them. Firm Y earns profits from a subsidy it obtained after large campaign contributions. '
          'Which statement is correct?',
     'opts': ["Y's gain reflects political favor, and its project may be counterproductive",
              'Both firms are market entrepreneurs, since both earn a profit in the end',
              "X's gain is crony capitalism, since its profit depends on low input costs",
              "Y's gain is efficient, since the subsidy was approved by elected officials"],
     'exp': 'X is a market entrepreneur, profiting by producing goods valued above their resource '
            'cost. Y is a crony capitalist, profiting from a political favor obtained with '
            'contributions, and such projects are often counterproductive.',
     'why': [None,
             "Profit alone doesn't make someone a market entrepreneur. Y's profit comes from a "
             'political favor, not from creating value for consumers.',
             'X profits by producing something buyers value more than it costs, which is market '
             'entrepreneurship. Crony capitalism means profiting from political favors.',
             "Approval by officials doesn't make a project efficient. Favors exchanged for campaign "
             'contributions often fund counterproductive projects.']},
    # id 257
    {'ch': 6,
     'q': 'A large toymaker backs a child-safety law requiring expensive testing that its smaller '
          'rivals must pay outside labs to perform, and parent groups enthusiastically support the '
          'law. What does this best illustrate?',
     'opts': ["Bootleggers and Baptists: a firm's gain packaged as a moral cause",
              'An external benefit: the testing protects children of other buyers',
              'A Type 4 project: widespread benefits with costs on the large firm',
              "Rational ignorance: parents don't know which toys contain lead"],
     'exp': "The large firm gains by raising its rivals' costs, while the safety framing wins "
            'enthusiastic support from parents. That is the bootlegger-and-Baptist strategy behind '
            'much crony capitalism.',
     'why': [None,
             'The safety benefit is the moral cover, not the explanation. The key point is that the '
             "large firm gains by raising its smaller rivals' costs.",
             "The large firm isn't the one bearing the cost; it gains. Most of the testing costs fall "
             'on smaller rivals who must pay outside labs.',
             'The parents actively support the law rather than ignoring it. What matters is that a '
             "firm's self-interest is packaged as a safety cause."]},
    # id 258
    {'ch': 6,
     'q': "Statement I: In the political sector, influence depends mainly on each person's single "
          'vote, so it is spread about equally. Statement II: In the market sector, people with larger '
          'incomes can buy more goods and services.',
     'opts': ['Statement I is false and Statement II is true',
              'Both Statement I and Statement II are true',
              'Statement I is true and Statement II is false',
              'Both Statement I and Statement II are false'],
     'exp': 'Political influence goes to those most able and willing to contribute time, persuasion, '
            'organization, and money to help politicians win, so Statement I is false. In markets, '
            'larger incomes buy more, so Statement II is true.',
     'why': [None,
             'Statement I is false. Each person has one vote, but influence also depends on time, '
             'organization, persuasion, and money, which are not spread equally.',
             'Both judgments are reversed. Political influence is not spread equally, while market '
             'purchasing power does rise with income.',
             'Statement II is true: in the marketplace, people with larger incomes can buy more goods '
             'and services.']},
    # id 259
    {'ch': 6,
     'q': 'A classmate argues: "Markets fail because of externalities and public goods, so moving a '
          'decision to government will make the outcome efficient." What is wrong with this reasoning?',
     'opts': ['Government has its own failures, such as special interests and rent seeking',
              'Externalities and public goods are not real sources of market failure',
              'Government corrects externalities well, but public goods are best left to markets',
              'Market failures correct themselves over time, so government adds little'],
     'exp': 'Both sectors have shortcomings. The special interest effect, the shortsightedness effect, '
            'rent seeking, and weak incentives for efficiency cause government failure, so improving '
            'outcomes means comparing both sectors.',
     'why': [None,
             'Externalities and public goods are genuine sources of market failure. The flaw is '
             'assuming that moving the decision to government fixes them automatically.',
             'This still assumes government reliably fixes some problems. Government failure can '
             'affect any decision moved into the political process.',
             "The text doesn't say market failures correct themselves. The point is that government "
             'has its own failures, so neither sector is automatically better.']},
    # id 260
    {'ch': 7,
     'q': 'Use the table. What was the growth rate of real GDP from 2024 to 2025?',
     'opts': ['10.0%', '15.5%', '10.5%', '5.0%'],
     'exp': 'Real GDP in 2025 = 2,310 / 1.05 = 2,200 in 2024 prices. Real growth = (2,200 - 2,000) / '
            '2,000 = 10.0%.',
     'why': [None,
             'This is nominal growth: (2,310 - 2,000) / 2,000 = 15.5%. It skips deflating 2025 nominal '
             'GDP, so it mixes higher output with higher prices.',
             'This subtracts the 5% price rise from 15.5% nominal growth. That shortcut is only '
             'approximate; dividing 2,310 by 1.05 gives the exact 10.0%.',
             'This is the change in the GDP deflator, from 100 to 105, which is the inflation rate, '
             'not the growth of real output.'],
     'fig': {'type': 'table',
             'head': ['Year', 'Nominal GDP ($ billions)', 'GDP deflator'],
             'rows': [['2024', '2,000', '100'], ['2025', '2,310', '105']],
             'alt': 'Table with two years. 2024: nominal GDP 2,000 billion dollars, GDP deflator 100. '
                    '2025: nominal GDP 2,310 billion dollars, GDP deflator 105.'}},
    # id 261
    {'ch': 7,
     'q': 'Use the table of consumer price index values. What was the inflation rate during 2025?',
     'opts': ['4.0%', '4.2%', '9.2%', '5.0%'],
     'exp': 'Inflation in 2025 = (218.4 - 210.0) / 210.0 x 100 = 4.0%. The percentage change is '
            "measured from the previous year's index.",
     'why': [None,
             'This is 8.4 / 200 = 4.2%: the right change in the index, but divided by the 2023 value '
             'instead of the 2024 value. The base must be the previous year.',
             'This is (218.4 - 200) / 200 = 9.2%, the cumulative change over two years, 2023 to 2025, '
             'not the inflation rate during 2025 alone.',
             'This is (210 - 200) / 200 = 5.0%, the inflation rate during 2024. It uses the wrong pair '
             'of years.'],
     'fig': {'type': 'table',
             'head': ['Year', 'CPI'],
             'rows': [['2023', '200.0'], ['2024', '210.0'], ['2025', '218.4']],
             'alt': 'Table of CPI values: 2023 is 200.0, 2024 is 210.0, 2025 is 218.4.'}},
    # id 262
    {'ch': 7,
     'q': "Use the table. A grandparent's job paid $12,000 in 1980, and the same job pays $40,000 "
          'today. Which statement about purchasing power is correct?',
     'opts': ['The 1980 pay equals about $45,000 today, so it bought more',
              "The 1980 pay equals about $3,200 today, so today's pay buys more",
              "The 1980 pay equals about $36,900 today, so today's pay buys more",
              "The 1980 pay equals about $33,000 today, so today's pay buys more"],
     'exp': "Convert to today's dollars: 12,000 x (307.5 / 82.0) = 12,000 x 3.75 = $45,000. That is "
            "more than today's $40,000, so the 1980 pay had more purchasing power.",
     'why': [None,
             'This flips the ratio: 12,000 x (82.0 / 307.5) = $3,200. Inflating earlier data to '
             'current dollars multiplies by current CPI over earlier CPI, not the reverse.',
             'This multiplies by 307.5 / 100 = 3.075, treating 1980 as the base year with CPI 100. The '
             '1980 CPI is 82.0, so the ratio must be 307.5 / 82.0.',
             "This multiplies $12,000 by the CPI's 275% increase, (307.5 - 82.0) / 82.0, and forgets "
             'to add back the original $12,000. Multiplying by 1 + 2.75 = 3.75 gives $45,000.'],
     'fig': {'type': 'table',
             'head': ['Year', 'CPI', 'Salary'],
             'rows': [['1980', '82.0', '$12,000'], ['Today', '307.5', '$40,000']],
             'alt': 'Table: in 1980 the CPI was 82.0 and the salary was 12,000 dollars. Today the CPI '
                    'is 307.5 and the salary is 40,000 dollars.'}},
    # id 263
    {'ch': 7,
     'q': "Use the table of this year's transactions for a small economy. What is GDP?",
     'opts': ['$1,130 billion', '$1,250 billion', '$1,350 billion', '$1,440 billion'],
     'exp': 'Using the expenditure approach: 700 + 200 + 250 + (90 - 110) = $1,130 billion. Used cars, '
            'Social Security transfers, and steel used to build cars are all left out.',
     'why': [None,
             'This adds the $120 billion of Social Security payments. Those are transfer payments, not '
             'purchases of current output, so they are excluded.',
             'This adds imports instead of subtracting them: 700 + 200 + 250 + 90 + 110 = 1,350. Net '
             'exports are exports minus imports, here -20.',
             'This adds every excluded item to 1,130: Social Security transfers (120), used cars '
             'produced in earlier years (40), and the intermediate steel (150), for 310 too much.'],
     'fig': {'type': 'table',
             'head': ['Item', '$ billions'],
             'rows': [['Household purchases of new goods and services', '700'],
                      ['Household purchases of used cars', '40'],
                      ['Gross private investment', '200'],
                      ['Government purchases of goods and services', '250'],
                      ['Social Security payments to retirees', '120'],
                      ['Exports', '90'],
                      ['Imports', '110'],
                      ['Steel bought by automakers to build new cars', '150']],
             'alt': 'Table of eight items in billions of dollars: household purchases of new goods and '
                    'services 700; household purchases of used cars 40; gross private investment 200; '
                    'government purchases of goods and services 250; Social Security payments to '
                    'retirees 120; exports 90; imports 110; steel bought by automakers to build new '
                    'cars 150.'}},
    # id 264
    {'ch': 7,
     'q': "Which of these transactions adds to this year's GDP?",
     'opts': ['A house built this year that the builder has not yet sold',
              'A 2015 house resold this year for more than its original price',
              'Flour a bakery buys this year to bake bread it sells this year',
              'A monthly government payment to a retiree from Social Security'],
     'exp': 'A house built this year is current production of a final good. Even unsold, it is counted '
            "as gross private investment through the builder's inventory.",
     'why': [None,
             'The house was produced in 2015 and counted then. Reselling it at a higher price involves '
             "no new production, so the sale does not add to this year's GDP.",
             'Flour used to bake bread is an intermediate good. Its value is already embodied in the '
             'price of the bread, so counting it too would double count.',
             'Social Security payments are transfers, not purchases of goods or services, so they are '
             'not part of government purchases or GDP.']},
    # id 265
    {'ch': 7,
     'q': 'A farmer sells wheat to a miller for $1. The miller sells the flour to a baker for $3. The '
          'baker sells the bread to a customer for $6. A classmate says these sales add $10 to GDP. '
          'What is wrong with this reasoning?',
     'opts': ['Only the $6 final sale counts; adding all three double counts the wheat and flour',
              'Only the $1 wheat sale counts, since it is the raw material behind all later sales',
              'Only the $9 from the miller and baker counts, since farm output is not in GDP',
              'Only the $5 increase from wheat to bread counts, so the $1 farm sale is dropped'],
     'exp': 'GDP counts only the final-user good. The $6 price of the bread already embodies the value '
            'of the wheat and the flour, so adding all three sales to get $10 counts them more than '
            'once.',
     'why': [None,
             "The wheat is an intermediate good; its value is part of the bread's $6 price. Counting "
             'only the first stage leaves out most of the value added by milling and baking.',
             'This adds $3 + $6 = $9, which still double counts the flour, an intermediate good. Farm '
             'output is not left out of GDP; it is counted inside the price of the final good.',
             "This computes $6 - $1 = $5, dropping the farmer's share. The farmer's $1 of value is "
             "part of the bread's $6 price, so the full $6 counts."]},
    # id 266
    {'ch': 7,
     'q': 'Country A cracks down on tax evasion, and many contractors who had been paid in unreported '
          'cash start reporting their work. The amount of construction actually done does not change. '
          'What happens to measured GDP?',
     'opts': ['It rises, because work hidden in the underground economy is now recorded',
              'It is unchanged, because the amount of construction done stayed the same',
              'It falls, because contractors now pay more in taxes on the same work',
              'It rises, because the extra tax revenue is added to government purchases'],
     'exp': 'Activity concealed to evade taxes is part of the underground economy and is missed by '
            'GDP. Once the same work is reported, measured GDP rises even though actual production did '
            'not change.',
     'why': [None,
             'Actual construction did not change, but GDP measures only recorded activity. Moving work '
             'out of the underground economy raises the measured figure.',
             'Taxes paid on the work do not subtract from GDP. The work itself is now recorded, so '
             'measured GDP goes up, not down.',
             'Tax revenue is not a government purchase of goods and services. The rise in measured GDP '
             'comes from the newly reported construction, not from taxes collected.']},
    # id 267
    {'ch': 7,
     'q': 'A firm builds a new factory this year. Statement I: The wages paid to the construction '
          'workers show up in the resource cost-income approach. Statement II: In the expenditure '
          'approach, the factory is counted as government purchases.',
     'opts': ['Statement I is true and Statement II is false',
              'Statement I is false and Statement II is true',
              'Both Statement I and Statement II are true',
              'Both Statement I and Statement II are false'],
     'exp': 'Wages paid to construction workers are employee compensation, a resource cost-income '
            'component, so I is true. A factory built by a private firm is gross private investment, '
            'so II is false.',
     'why': [None,
             'Statement I was misjudged: wages are employee compensation, part of the resource '
             'cost-income approach. Statement II was also misjudged: a private factory is investment, '
             'not government purchases.',
             'Statement II is false: government purchases are spending by governments. A factory paid '
             'for by a private firm is counted as gross private investment.',
             'Statement I is true: wages paid in producing the factory are employee compensation, one '
             'of the direct cost-income components of GDP.']},
    # id 268
    {'ch': 7,
     'q': 'Countries X and Y have the same real GDP per person. Workers in X average 55-hour weeks '
          'with little vacation, while workers in Y average 38-hour weeks. What does this comparison '
          'show about GDP as a welfare measure?',
     'opts': ['Y is likely better off, since GDP leaves out leisure and the strain of extra work',
              'X is likely better off, since GDP adds value for the extra hours people work',
              'Both are equally well off, since equal real GDP per person means equal welfare',
              'Y is likely worse off, since its shorter weeks are subtracted from its GDP'],
     'exp': 'GDP excludes leisure and the human costs of producing goods and services. Y produces the '
            'same output per person with far fewer hours, so it is likely better off.',
     'why': [None,
             'GDP does not add any value for hours worked; it counts only the market value of output. '
             'Longer hours with the same output mean less leisure, not more welfare.',
             'Equal real GDP per person is only a broad indicator. Because GDP leaves out leisure and '
             'human costs, the same GDP can hide large differences in well-being.',
             'Nothing is subtracted from GDP for shorter workweeks. GDP simply ignores leisure, which '
             "is why Y's extra free time does not show up as a gain."]},
    # id 269
    {'ch': 7,
     'q': 'Prices of new industrial machinery made and sold in the U.S. rise sharply, while prices of '
          'everything households buy stay the same. What happens to the two price indexes?',
     'opts': ['The GDP deflator rises while the consumer price index stays about the same',
              'The consumer price index rises while the GDP deflator stays about the same',
              'Both indexes rise by the same amount because they track the same prices',
              'Both indexes stay the same because machinery is an intermediate good'],
     'exp': 'New machinery is a final investment good and part of the GDP bundle, so the broader GDP '
            'deflator rises. The CPI tracks only the household bundle, whose prices did not change.',
     'why': [None,
             'This reverses the coverage. Households do not buy industrial machinery, so the CPI does '
             'not include it; the GDP deflator does.',
             'The two indexes use different baskets: everything in GDP versus what households buy. A '
             'price change in a good outside the household bundle moves only the deflator.',
             'New machinery bought by firms is a final good counted as gross private investment, not '
             'an intermediate good used up in production. Its price is in the deflator.']},
    # id 270
    {'ch': 7,
     'q': 'The price of beef jumps 30% while chicken prices hold steady, and shoppers switch toward '
          'chicken. Which index will most likely report the highest inflation for this period?',
     'opts': ['The traditional CPI, whose basket still holds the old amount of beef',
              'The chained CPI, whose basket now holds the extra chicken purchases',
              'The GDP deflator, because its broad basket includes more beef',
              'The three equally, since each one tracks the same beef prices'],
     'exp': 'The traditional CPI keeps the old basket quantities, so it still weights beef heavily and '
            'overstates the rise in living costs. Indexes that adjust for substitution report less '
            'inflation.',
     'why': [None,
             'The chained CPI is the one that adjusts quantities monthly for substitution toward '
             'cheaper goods, so it reports slightly lower inflation than the traditional CPI.',
             'The GDP deflator also accounts for substitution away from relatively pricier goods, so '
             'it, like the chained CPI, generally reports slightly lower inflation than the '
             'traditional CPI.',
             'The indexes use different baskets and procedures. Because only the traditional CPI '
             'ignores the switch to chicken, it reports the highest inflation.']},
    # id 271
    {'ch': 7,
     'q': "Statement I: When a factory's output rises and its extra pollution damages a nearby river, "
          'GDP counts the added output with no deduction for the damage. Statement II: When employees '
          'work extra overtime, GDP counts the added output with no deduction for the leisure they '
          'give up.',
     'opts': ['Both Statement I and Statement II are true',
              'Statement I is true and Statement II is false',
              'Statement I is false and Statement II is true',
              'Both Statement I and Statement II are false'],
     'exp': 'GDP makes no adjustment for harmful side effects of production, so I is true. GDP also '
            'excludes leisure and the human costs of producing output, so II is true.',
     'why': [None,
             'Statement II is true: GDP counts the added output from overtime with no deduction for '
             'lost leisure, because it excludes leisure and human costs entirely.',
             'Statement I is true: GDP has no deduction for pollution or other economic bads, so the '
             'extra output counts in full.',
             'Both shortcomings are real. GDP neither subtracts pollution damage nor deducts the '
             'leisure people give up, which is why rising GDP can overstate gains in well-being.']},
    # id 272
    {'ch': 7,
     'q': 'A parent who earned $50,000 quits to stay home and care for their child, who had been in a '
          '$15,000-a-year daycare. What happens to measured GDP, and why?',
     'opts': ['It falls, though the child care is still produced, now outside the market',
              'It rises, since the family no longer spends $15,000 a year on paid daycare',
              'It is unchanged, since the same child care is produced either way',
              'It falls by $15,000, the market value of the daycare services lost'],
     'exp': "Both the parent's $50,000 of paid output and the $15,000 daycare purchase drop out of "
            'GDP. The child care continues as household production, which GDP does not count.',
     'why': [None,
             'Spending less on daycare lowers GDP, because the daycare purchase was part of '
             'consumption. Nothing new is added, since home child care is not a market transaction.',
             'The same care is produced, but at home it is nonmarket production, which GDP excludes. '
             'Moving it out of the market lowers measured GDP.',
             "This counts only the daycare. The parent's $50,000 of paid work also leaves GDP, so "
             'measured GDP falls by more than $15,000.']},
    # id 273
    {'ch': 7,
     'q': "This year's laptops cost the same as last year's but are twice as powerful. If the price "
          'index treats them as the same product at the same price, what is the likely error?',
     'opts': ['Inflation is overstated and real output growth is understated',
              'Inflation is understated and real output growth is overstated',
              'Nominal GDP is overstated, while real GDP is measured correctly',
              "Neither is distorted, since the laptop's price did not change"],
     'exp': 'Twice the power at the same price means the quality-adjusted price fell. Ignoring that '
            'reports too much inflation, and deflating nominal GDP by a too-high price index '
            'understates real output growth.',
     'why': [None,
             'This reverses both errors. Missing a quality improvement makes the price index too high, '
             'so inflation is overstated and real growth is understated.',
             'Nominal GDP is measured at actual market prices, so it is not distorted. The error '
             'enters through the price index, which then distorts real GDP.',
             'The sticker price is unchanged, but the product is better. Accurate real GDP requires '
             'measuring price changes including quality, so ignoring the improvement does distort the '
             'numbers.']},
    # id 274
    {'ch': 7,
     'q': "A country's real GDP grows 2% this year while its population grows 3%. What happens to real "
          'GDP per capita?',
     'opts': ['It falls by about 1%',
              'It rises by about 1%',
              'It rises by about 5%',
              'It rises by about 2%'],
     'exp': 'Per capita GDP is GDP divided by population. Output grew 2% while population grew 3%, so '
            'output per person falls by about 2% - 3% = -1%.',
     'why': [None,
             'This is a sign error: it subtracts GDP growth from population growth (3% - 2%) instead '
             'of population growth from GDP growth.',
             'This adds population growth to GDP growth. A larger population divides output among more '
             'people, so its growth must be subtracted.',
             'This ignores the population change and reports total real GDP growth. Per capita GDP '
             'divides by population, which grew faster than output.']},
    # id 275
    {'ch': 8,
     'q': "Use the table for an economy's adults aged 16 and older. What is the unemployment rate?",
     'opts': ['10.0%', '6.5%', '11.1%', '35.0%'],
     'exp': 'Labor force = 117 + 13 = 130 million. Unemployment rate = unemployed / labor force = 13 / '
            '130 = 10.0%.',
     'why': [None,
             'This divides by the whole adult population, 13 / 200 = 6.5%. The denominator must be the '
             'labor force, which excludes the 70 million not in the labor force.',
             'This divides by the employed only, 13 / 117 = 11.1%. The labor force includes both the '
             'employed and the unemployed.',
             'This is 70 / 200 = 35.0%, the share of adults not in the labor force. It is not the '
             'unemployment rate.'],
     'fig': {'type': 'table',
             'head': ['Group', 'Millions of people'],
             'rows': [['Employed', '117'], ['Unemployed', '13'], ['Not in the labor force', '70']],
             'alt': 'Table: employed 117 million, unemployed 13 million, not in the labor force 70 '
                    'million.'}},
    # id 276
    {'ch': 8,
     'q': 'An economy has 240 million people aged 16 and older. Of these, 144 million are employed and '
          '12 million are unemployed. What are the labor force participation rate and the '
          'employment-population ratio?',
     'opts': ['65.0% and 60.0%', '60.0% and 65.0%', '65.0% and 92.3%', '7.7% and 60.0%'],
     'exp': 'Labor force = 144 + 12 = 156 million. Participation rate = 156 / 240 = 65.0%, and the '
            'employment-population ratio = 144 / 240 = 60.0%.',
     'why': [None,
             'These are the right numbers in the wrong order. Participation uses the labor force '
             '(156), and the employment-population ratio uses the employed (144), both over 240.',
             'The 92.3% is 144 / 156, employed divided by the labor force. The employment-population '
             'ratio divides the employed by the whole 16-and-older population, 240.',
             'The 7.7% is 12 / 156, the unemployment rate. Participation divides the labor force, 156, '
             'by the population of 240.']},
    # id 277
    {'ch': 8,
     'q': "Use the table of a small town's residents aged 16 and older. Using the official "
          "definitions, what is the town's unemployment rate?",
     'opts': ['13.3%', '26.7%', '17.7%', '5.8%'],
     'exp': 'Employed = 50 + 10 + 5 = 65; unemployed = 6 on layoff + 4 searching = 10. Labor force = '
            '75, so the rate is 10 / 75 = 13.3%.',
     'why': [None,
             'This counts the 10 part-timers seeking full-time work as unemployed: 20 / 75 = 26.7%. '
             'Anyone working for pay at least one hour a week is employed.',
             'This adds the 4 people who stopped looking: 14 / 79 = 17.7%. Wanting a job without '
             'actively seeking one puts a person outside the labor force.',
             'This leaves out the 6 laid-off workers: 4 / 69 = 5.8%. People on layoff waiting to '
             'return to a previous job count as unemployed.'],
     'fig': {'type': 'table',
             'head': ['Residents', 'Number'],
             'rows': [['Working full-time for pay', '50'],
                      ['Working part-time for pay and looking for full-time work', '10'],
                      ['Working 20 hours a week unpaid on the family farm', '5'],
                      ['On layoff, expecting to be recalled', '6'],
                      ['Not working and actively applying for jobs', '4'],
                      ['Want a job but have not looked in months', '4'],
                      ['Full-time students not working or looking', '12'],
                      ['Retired', '8']],
             'alt': 'Table of 99 residents: 50 working full-time for pay; 10 working part-time for pay '
                    'and looking for full-time work; 5 working 20 hours a week unpaid on the family '
                    'farm; 6 on layoff expecting recall; 4 not working and actively applying for jobs; '
                    '4 who want a job but have not looked in months; 12 full-time students not working '
                    'or looking; 8 retired.'}},
    # id 278
    {'ch': 8,
     'q': "A teenager works 10 hours a week without pay in his parents' hardware store and is not "
          'looking for any other job. How is he classified?',
     'opts': ['Not in the labor force',
              'Employed as family help',
              'Unemployed, since unpaid',
              'Employed part-time, unpaid'],
     'exp': 'Unpaid family work counts as employment only at 15 or more hours a week. At 10 hours, and '
            'with no job search, he is neither employed nor unemployed, so he is not in the labor '
            'force.',
     'why': [None,
             'Unpaid family help counts as employed only at 15 or more hours a week. Ten hours falls '
             'short of that threshold.',
             'To be unemployed he would need to be seeking a job, waiting to start one, or on layoff. '
             'He is not looking for work.',
             'There is no unpaid part-time employment category. Unpaid work counts only in a family '
             'enterprise at 15 or more hours a week.']},
    # id 279
    {'ch': 8,
     'q': 'Ana quits her accounting job to search for a better-paying one. Ben, a typesetter, loses '
          'his job when software replaces his trade. Cal is laid off from a furniture plant when sales '
          'drop across the economy in a recession. Which classification is correct?',
     'opts': ['Ana frictional, Ben structural, Cal cyclical',
              'Ana structural, Ben frictional, Cal cyclical',
              'Ana frictional, Ben cyclical, Cal structural',
              'Ana cyclical, Ben structural, Cal frictional'],
     'exp': "Ana is job shopping with imperfect information: frictional. Ben's skills are no longer "
            'demanded because of new technology: structural. Cal lost his job in a general downturn: '
            'cyclical.',
     'why': [None,
             'Ana and Ben are swapped. Ana could find a job with better information, which is '
             "frictional; Ben's skills became obsolete, which is structural.",
             'Ben and Cal are swapped. Ben lost his job to technology, a structural change; Cal lost '
             'his job to a general recession, which is cyclical.',
             'Ana and Cal are swapped. Voluntarily searching for a better job is frictional, while '
             'layoffs from an economy-wide drop in sales are cyclical.']},
    # id 280
    {'ch': 8,
     'q': 'A news report says the unemployment rate is 4.5%. A classmate concludes that 4.5% of all '
          'adults have no job. What is wrong with this reasoning?',
     'opts': ['The rate is a share of the labor force, and retirees and students without jobs are not '
              'in it',
              'The rate is a share of the total population, including children under 16 who cannot '
              'work',
              'The rate is a share of the employed, so it compares job seekers with people holding '
              'jobs',
              'The rate measures cyclical unemployment, leaving frictional and structural out'],
     'exp': 'The unemployment rate divides the unemployed by the labor force, which leaves out people '
            'neither working nor seeking work, such as retirees, students, and homemakers. Far more '
            'than 4.5% of adults lack jobs.',
     'why': [None,
             'The population counted starts at age 16, and the denominator is the labor force, not the '
             'total population. Children are not part of the calculation at all.',
             'The denominator is the labor force, employed plus unemployed, not the employed alone. '
             'And this still does not explain why jobless adults outside the labor force are missed.',
             'The unemployment rate counts all unemployed people, including frictional and structural '
             'unemployment, not only the cyclical part.']},
    # id 281
    {'ch': 8,
     'q': 'Statement I: A rise in the share of young workers in the labor force tends to raise the '
          'natural rate of unemployment. Statement II: More generous unemployment benefits tend to '
          'lower the natural rate of unemployment.',
     'opts': ['Statement I is true and Statement II is false',
              'Statement I is false and Statement II is true',
              'Both Statement I and Statement II are true',
              'Both Statement I and Statement II are false'],
     'exp': 'Young workers switch jobs and job shop more, so a larger share of them raises the natural '
            'rate: I is true. More generous unemployment benefits make longer searches cheaper and '
            'tend to raise it: II is false.',
     'why': [None,
             'Statement I was misjudged: young workers job shop more, so a larger share of them raises '
             'the natural rate. Statement II was also misjudged: generous benefits raise it.',
             'Statement II is false: more generous unemployment benefits reduce the cost of searching '
             'longer, which tends to raise the natural rate, not lower it.',
             'Statement I is true: young workers change jobs more often, so a larger share of them '
             'pushes the natural rate up.']},
    # id 282
    {'ch': 8,
     'q': 'The natural rate of unemployment is 4.5%, but the actual unemployment rate has fallen to '
          '3.5%. What does this suggest about the economy?',
     'opts': ['It is in a boom, with actual GDP temporarily above potential GDP',
              'It is in a recession, with actual GDP well below potential GDP',
              'It is at full employment, with cyclical unemployment equal to zero',
              'It has a permanently higher potential output and a lower natural rate'],
     'exp': 'Actual unemployment falls below the natural rate during a boom, when actual output '
            'temporarily exceeds potential, the maximum sustainable level.',
     'why': [None,
             'In a recession actual unemployment rises above the natural rate. Here it is below the '
             'natural rate, which is the boom case.',
             'Full employment means the actual rate equals the natural rate. A rate 1 point below the '
             'natural rate is a temporary low, not full employment.',
             'A temporary dip below the natural rate reflects a boom, not a permanent change. The '
             'natural rate is the sustainable rate, which actual unemployment cannot stay below.']},
    # id 283
    {'ch': 8,
     'q': 'The natural rate of unemployment is 5%, and during a recession the actual rate rises to 8%. '
          'Which statement is correct?',
     'opts': ['Cyclical unemployment is 3 points, and actual GDP is below potential',
              'Cyclical unemployment is 8 points, and actual GDP is below potential',
              'Cyclical unemployment is 3 points, and actual GDP is above potential',
              'Cyclical unemployment is 5 points, and actual GDP equals potential'],
     'exp': 'The natural rate covers frictional and structural unemployment, so cyclical unemployment '
            'is 8 - 5 = 3 percentage points. In a recession actual GDP is below potential.',
     'why': [None,
             'This counts all 8 points as cyclical. The 5% natural rate of frictional and structural '
             'unemployment remains in every phase, so only the excess is cyclical.',
             'The 3 points is right, but the GDP direction is reversed. Unemployment above the natural '
             'rate means actual output is below potential.',
             'This takes the natural rate itself as the cyclical part. The 5% is frictional and '
             'structural; actual GDP equals potential only when unemployment is at 5%.']},
    # id 284
    {'ch': 8,
     'q': 'The graph shows real GDP over time along with its long-run trend. Which phase of the '
          'business cycle is the economy in at each labeled point?',
     'opts': ['A contraction, B trough, C expansion, D peak',
              'A peak, B contraction, C trough, D expansion',
              'A expansion, B trough, C contraction, D peak',
              'A trough, B contraction, C peak, D expansion'],
     'exp': 'The phase depends on the direction real GDP is moving. A is on a falling stretch '
            '(contraction), B is the bottom (trough), C is on a rising stretch (expansion), and D is '
            'the top (peak).',
     'why': [None,
             'This lists the phases in memorized order starting at A. But A is on a falling stretch, '
             'not at a top, so A is a contraction, not a peak.',
             'A and C are swapped. A sits on a falling stretch of real GDP, so it is a contraction; C '
             'sits on a rising stretch, so it is an expansion.',
             'A is on a falling stretch, so it is a contraction, not a trough; the trough is B, the '
             'lowest point. C is on a rising stretch (expansion), and D, the top of the rise, is the '
             'peak. Read whether real GDP is rising or falling at each point.'],
     'fig': {'type': 'graph',
             'x': 'Time',
             'y': 'Real GDP',
             'lines': [{'pts': [[8, 20], [92, 57.8]], 'cls': 'm', 'label': 'Trend'},
                       {'pts': [[8, 20],
                                [14, 30.3],
                                [20, 37.8],
                                [26, 40.5],
                                [32, 38.4],
                                [38, 33.5],
                                [44, 28.6],
                                [50, 26.5],
                                [56, 29.2],
                                [62, 36.7],
                                [68, 47.0],
                                [74, 57.3],
                                [80, 64.8],
                                [86, 67.5],
                                [92, 65.4]],
                        'cls': 'd',
                        'label': 'Real GDP'}],
             'points': [{'at': [38, 33.5], 'label': 'A'},
                        {'at': [50, 26.5], 'label': 'B'},
                        {'at': [68, 47.0], 'label': 'C'},
                        {'at': [86, 67.5], 'label': 'D'}],
             'guides': False,
             'alt': 'A wavy real GDP curve rises and falls around a straight, upward-sloping trend '
                    'line over time. Point A is on a falling stretch of the curve, where it crosses '
                    'the trend line. Point B is the lowest point of the dip that follows. Point C is '
                    'on a rising stretch, where the curve crosses the trend line again. Point D is the '
                    'high point at the top of the next rise.'}},
    # id 285
    {'ch': 8,
     'q': 'The graph shows potential GDP and actual GDP over time. Which statement about the labeled '
          'points is correct?',
     'opts': ['At F unemployment is above the natural rate, and G is at full employment',
              'At E unemployment is above the natural rate, and G is at full employment',
              'At F unemployment is above the natural rate, and E is at full employment',
              'At E unemployment is below the natural rate, and F is at full employment'],
     'exp': 'Where actual GDP is below potential, as at F, unemployment exceeds the natural rate. '
            'Actual and potential output are equal only at full employment, which is point G.',
     'why': [None,
             'At E actual GDP is above potential, a boom, so unemployment is below the natural rate, '
             'not above it.',
             'F is correct, but E is not full employment: actual GDP is above potential there. Full '
             'employment is where actual equals potential, at G.',
             'E is correct, but F is below potential, a slump with unemployment above the natural '
             'rate. Full employment is at G, where the curves cross.'],
     'fig': {'type': 'graph',
             'x': 'Time',
             'y': 'Real GDP',
             'lines': [{'pts': [[10, 25], [90, 70]], 'cls': 'v', 'label': 'Potential'},
                       {'pts': [[10, 25],
                                [15, 32.5],
                                [20, 38.2],
                                [22.5, 40.0],
                                [25, 41.0],
                                [30, 41.0],
                                [35, 39.1],
                                [40, 37.2],
                                [45, 37.1],
                                [47.5, 38.1],
                                [50, 39.9],
                                [55, 45.6],
                                [60, 53.1],
                                [65, 60.6],
                                [70, 66.4]],
                        'cls': 'd',
                        'label': 'Actual'}],
             'points': [{'at': [22.5, 40.0], 'label': 'E'},
                        {'at': [35, 39.1], 'label': 'G'},
                        {'at': [47.5, 38.1], 'label': 'F'}],
             'guides': False,
             'alt': 'A straight upward-sloping potential GDP line and a wavy actual GDP curve over '
                    'time. At point E the actual GDP curve is above the potential GDP line. At point G '
                    'the actual GDP curve crosses the potential GDP line. At point F the actual GDP '
                    'curve is below the potential GDP line.'}},
    # id 286
    {'ch': 8,
     'q': 'A recession ends in June, and real GDP starts growing again. Based on the U.S. record since '
          '1960, what typically happens to the unemployment rate around this turning point?',
     'opts': ['It soon starts falling, but it stays above the natural rate for a while',
              'It drops back to the natural rate as soon as real GDP starts to grow',
              'It keeps climbing for years, until real GDP is back at its prior peak',
              'It soon falls below the natural rate as firms rehire laid-off workers'],
     'exp': 'Since 1960, the unemployment rate began falling soon after each expansion started, but it '
            'stayed above the natural rate during and immediately after each recession.',
     'why': [None,
             'The record shows unemployment stayed above the natural rate immediately after each '
             'recession. Job recovery lags the turn in real GDP.',
             'Unemployment began to decline soon after each expansion started; it did not keep rising '
             'for years until GDP regained its prior peak.',
             'Unemployment falls below the natural rate only in a boom. Right after a recession it '
             'remains above the natural rate for a while.']},
    # id 287
    {'ch': 8,
     'q': 'A classmate argues: when inflation runs high, people learn to expect it and write it into '
          'their contracts, so high inflation does little harm. What is the main flaw in this '
          'argument?',
     'opts': ['High inflation is usually highly variable, so it is hard to anticipate',
              'High inflation is usually steady, so contracts are written too cautiously',
              'Anticipated inflation is what disrupts contracts, not the surprise part',
              'Contracts cannot include inflation, so even steady inflation is a surprise'],
     'exp': 'When inflation is high, its year-to-year changes are nearly always highly variable, so '
            'much of it comes as a surprise. Unanticipated inflation alters long-term contract '
            'outcomes, raising risk and slowing investment.',
     'why': [None,
             'This reverses the facts: high inflation is nearly always highly variable, not steady. '
             'That variability is why it cannot be reliably built into contracts.',
             'This reverses which kind of inflation does the harm. Anticipated inflation can be built '
             'into contracts; it is the unanticipated surprise that disrupts outcomes.',
             'Contracts can include expected inflation; that is what anticipated inflation means. The '
             'problem is that high inflation is too variable to anticipate accurately.']},
    # id 288
    {'ch': 8,
     'q': 'During a period of 8% inflation, a furniture maker sees the price of its tables rise 8% and '
          'hires more workers, thinking demand for tables has grown. Prices of everything else also '
          'rose 8%. Which harm of inflation does this illustrate?',
     'opts': ['Inflation distorts the information that prices deliver',
              'Inflation lowers potential output by shrinking the labor force',
              'Inflation raises structural unemployment in furniture making',
              'Inflation raises the risk of long-term investment projects'],
     'exp': "The table's relative price did not change, but the firm read a general price rise as a "
            'sign of stronger demand. Inflation distorted the information prices deliver.',
     'why': [None,
             'Nothing here changes the size of the labor force. The firm actually hired more workers; '
             'the harm is a poor production decision based on a misleading price signal.',
             "Structural unemployment involves a mismatch of skills. Nothing about workers' skills is "
             'involved; the firm misread a price signal.',
             'Higher risk on long-term projects comes from unanticipated changes in inflation. The '
             "firm's error here is mistaking a general price rise for a relative price rise."]},
    # id 289
    {'ch': 8,
     'q': "A country's central bank expands the money supply by 25% a year, while real output grows "
          'about 3% a year. What is the most likely result?',
     'opts': ['Rising prices, as aggregate demand grows faster than the supply of goods',
              'Falling prices, as the extra money raises output well above its potential',
              'Steady prices, since output is also growing and absorbs the extra money',
              'Rising unemployment, as businesses cut output in response to more money'],
     'exp': 'When aggregate demand rises faster than aggregate supply, prices rise. Money growing 25% '
            'a year while output grows only 3% means too much money chasing too few goods.',
     'why': [None,
             'Money growth far beyond output growth pushes prices up, not down. Output cannot stay '
             'above its sustainable potential just because there is more money.',
             'Output growth of 3% absorbs only a small part of 25% money growth. The large gap is the '
             'classic cause of inflation.',
             'More money raises spending and aggregate demand rather than cutting output. Rapid money '
             'growth is linked to inflation, not to firms cutting production.']},
    # id 290
    {'ch': 9,
     'q': 'In the graph, short-run equilibrium occurs at price level P1. Suppose the price level is '
          'currently P2 instead. What happens?',
     'opts': ['Quantity supplied at B exceeds quantity demanded at A, so the price level falls',
              'Quantity demanded at A exceeds quantity supplied at B, so the price level rises',
              'Quantity supplied at B exceeds quantity demanded at A, so the price level rises',
              'Firms earn high profits at P2, so the price level stays there in the short run'],
     'exp': 'At P2, buyers want only the output at A, while sellers want to supply the larger output '
            'at B. That excess supply pushes the price level down toward P1.',
     'why': [None,
             'This misreads the graph: at P2 the AD point A lies to the left of the SRAS point B. '
             'Excess demand occurs only at price levels below P1.',
             'Comparing B with A correctly shows excess supply, but excess supply pushes prices down, '
             'not up.',
             'P2 is not an equilibrium. With quantity supplied above quantity demanded, unsold output '
             'pushes the price level down regardless of profits.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD'},
                       {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS'},
                       {'pts': [[8, 70], [92, 70]], 'cls': 'm', 'label': ''}],
             'points': [{'at': [50, 50], 'label': 'E'},
                        {'at': [30, 70], 'label': 'A'},
                        {'at': [70, 70], 'label': 'B'}],
             'guides': True,
             'yticks': [[50, 'P1'], [70, 'P2']],
             'alt': 'A downward-sloping AD curve and an upward-sloping SRAS curve cross at point E at '
                    'price level P1. A horizontal line at the higher price level P2 meets AD at point '
                    'A on the left and SRAS at point B on the right.'}},
    # id 291
    {'ch': 9,
     'q': 'The economy is at point E in the graph. Which statement best describes this situation?',
     'opts': ['Unemployment is below the natural rate, and output Y1 cannot be sustained',
              'E is a long-run equilibrium, since the AD and SRAS curves intersect there',
              "Output Y1 is sustainable, because higher prices keep firms' profits high",
              'Unemployment is above the natural rate, since output differs from YF'],
     'exp': 'E is a short-run equilibrium to the right of LRAS, so output Y1 exceeds YF and '
            'unemployment is below the natural rate. That output can be reached temporarily, but '
            'resource prices rise as contracts expire, so it cannot be sustained.',
     'why': [None,
             'AD and SRAS crossing gives only a short-run equilibrium. Long-run equilibrium needs AD, '
             'SRAS, and LRAS to meet at one point, and E is off LRAS.',
             'The high profits at E come from costs fixed by contracts. When contracts expire, '
             'resource prices rise, margins shrink, and output returns to YF.',
             'The direction is reversed: Y1 is **above** YF, so unemployment is below the natural '
             'rate, not above it.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[35, 85], [95, 25]], 'cls': 'd', 'label': 'AD'},
                       {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS'},
                       {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
             'points': [{'at': [60, 60], 'label': 'E'}],
             'guides': True,
             'xticks': [[50, 'YF'], [60, 'Y1']],
             'yticks': [[60, 'P1']],
             'alt': 'AD and SRAS cross at point E at output Y1 and price level P1. A vertical LRAS '
                    'line stands at output YF, to the left of Y1.'}},
    # id 292
    {'ch': 9,
     'q': 'In the graph, AD, SRAS, and LRAS all pass through point E. Statement I: At E, the actual '
          'price level equals the price level people anticipated when they signed their contracts. '
          'Statement II: At E, the unemployment rate is zero because output equals YF.',
     'opts': ['Statement I is true and Statement II is false',
              'Both Statement I and Statement II are true',
              'Statement I is false and Statement II is true',
              'Both Statement I and Statement II are false'],
     'exp': 'Long-run equilibrium requires that people correctly anticipated the price level when they '
            'made their agreements, so Statement I is true. Statement II is false: at YF the '
            'unemployment rate equals the natural rate, not zero.',
     'why': [None,
             'Statement II is false. At YF the actual unemployment rate equals the natural rate, which '
             'still includes frictional and structural unemployment.',
             'Both judgments are reversed. Correctly anticipating the price level is a requirement of '
             'long-run equilibrium, and unemployment at YF is the natural rate, not zero.',
             'Statement I is true: in long-run equilibrium the actual price level equals the level '
             'people anticipated when they signed their contracts.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD'},
                       {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS'},
                       {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
             'points': [{'at': [50, 50], 'label': 'E'}],
             'guides': True,
             'xticks': [[50, 'YF']],
             'yticks': [[50, 'P1']],
             'alt': 'A downward-sloping AD curve, an upward-sloping SRAS curve, and a vertical LRAS '
                    'line all pass through point E at output YF and price level P1.'}},
    # id 293
    {'ch': 9,
     'q': 'The graph shows the loanable funds market at E1, when people expect stable prices, and at '
          'E2, after borrowers and lenders come to expect 5% annual inflation. At E2, what are the '
          'money interest rate and the real interest rate?',
     'opts': ['Money rate 11%, real rate 6%',
              'Money rate 6%, real rate 11%',
              'Money rate 11%, real rate 11%',
              'Money rate 11%, real rate 5%'],
     'exp': 'The market rate at E2 on the graph is the money interest rate, 11%. Subtracting the 5% '
            'inflationary premium leaves a real rate of 6%, unchanged from E1.',
     'why': [None,
             'This swaps the two rates. The rate read off the graph is the money rate; the real rate '
             'is the money rate minus the inflationary premium.',
             'This forgets to subtract the inflationary premium. The real rate is 11% − 5% = 6%.',
             '5% is the expected inflation rate, which is the premium, not the real rate. The real '
             'rate is 11% − 5% = 6%.'],
     'fig': {'type': 'graph',
             'x': 'Quantity of loanable funds',
             'y': 'Interest rate',
             'lines': [{'pts': [[15, 75], [80, 10]], 'cls': 'm', 'label': 'D1'},
                       {'pts': [[20, 10], [85, 75]], 'cls': 'm', 'label': 'S1'},
                       {'pts': [[35, 80], [95, 20]], 'cls': 'd', 'label': 'D2', 'dash': True},
                       {'pts': [[8, 23], [75, 90]], 'cls': 's', 'label': 'S2', 'dash': True}],
             'points': [{'at': [50, 40], 'label': 'E1'}, {'at': [50, 65], 'label': 'E2'}],
             'guides': True,
             'yticks': [[40, '6%'], [65, '11%']],
             'alt': 'Original demand D1 and supply S1 for loanable funds cross at E1 at an interest '
                    'rate of 6%. New curves D2 and S2, each shifted upward, cross at E2 at an interest '
                    'rate of 11%, at the same quantity of funds as E1.'}},
    # id 294
    {'ch': 9,
     'q': 'The graph shows the market for foreign currency from the U.S. point of view. Which '
          'transactions lie behind the demand curve D and the supply curve S?',
     'opts': ['D: U.S. imports and capital outflow; S: U.S. exports and capital inflow',
              'D: U.S. exports and capital inflow; S: U.S. imports and capital outflow',
              'D: U.S. imports and capital inflow; S: U.S. exports and capital outflow',
              'D: U.S. exports and capital outflow; S: U.S. imports and capital inflow'],
     'exp': 'Americans demand foreign currency to buy imports and to invest abroad, which is capital '
            'outflow. Foreigners supply foreign currency when they buy U.S. exports and U.S. assets, '
            'which is capital inflow.',
     'why': [None,
             'This reverses both curves. Buying imports and investing abroad require foreign currency, '
             'so they belong on the demand side.',
             'The trade flows are placed correctly, but capital inflow belongs with supply: foreigners '
             'buying U.S. assets supply foreign currency to get dollars.',
             'The capital flows are placed correctly, but exports belong with supply: foreigners '
             'buying U.S. goods supply foreign currency to get dollars.'],
     'fig': {'type': 'graph',
             'x': 'Quantity of foreign currency',
             'y': 'Dollar price of foreign currency',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'D'},
                       {'pts': [[15, 15], [85, 85]], 'cls': 's', 'label': 'S'}],
             'points': [{'at': [50, 50], 'label': 'E'}],
             'guides': True,
             'xticks': [[50, 'Q*']],
             'alt': 'A downward-sloping demand curve D and an upward-sloping supply curve S for '
                    'foreign currency cross at point E at quantity Q*.'}},
    # id 295
    {'ch': 9,
     'q': 'A lender and a borrower agree on a one-year loan at a 9% money interest rate, both '
          'expecting 3% inflation. Actual inflation turns out to be 7%. What real interest rate did '
          'the lender actually earn, and who gained?',
     'opts': ["2%, and the borrower gained at the lender's expense",
              '6%, and neither gained since the rate was agreed upon',
              "2%, and the lender gained at the borrower's expense",
              "16%, and the lender gained at the borrower's expense"],
     'exp': 'The realized real rate is the money rate minus actual inflation: 9% − 7% = 2%. Because '
            'inflation was higher than expected, the borrower repaid with dollars worth less than '
            "planned and gained at the lender's expense.",
     'why': [None,
             '6% is 9% − 3%, the real rate they **expected**. A fixed money rate is exactly why '
             'surprise inflation shifts real gains to the borrower.',
             'The 2% is right, but the gain goes the other way: the lender expected a 6% real return '
             'and got only 2%, so the borrower gained.',
             'This adds inflation to the money rate instead of subtracting it and also reverses the '
             'winner; the real rate was 9% − 7% = 2%.']},
    # id 296
    {'ch': 9,
     'q': 'In 2025 a credit union made five-year fixed-rate car loans that built in an expected '
          'inflation rate of 4%. Over the following years, inflation averages only 1%. Which statement '
          'is correct?',
     'opts': ['The credit union gains, because borrowers repay in dollars worth more than expected',
              'Borrowers gain, because lower inflation reduces the money interest rate they owe',
              'Neither side gains, because the money interest rate was fixed in the contract',
              'Borrowers gain, because they repay in dollars with more purchasing power than planned'],
     'exp': "When actual inflation is lower than anticipated, lenders gain at borrowers' expense. The "
            '4% inflation premium built into the fixed rate turns out too high, so borrowers repay in '
            'dollars worth more than expected.',
     'why': [None,
             'The loans carry a fixed rate, so the money interest rate borrowers owe does not fall. '
             'Instead the real rate they pay rises, which hurts them.',
             'A fixed money rate is what makes the real rate change when inflation surprises. With '
             'inflation 3 points below expected, the real rate is higher than planned.',
             'Repaying in dollars with more purchasing power than planned is a cost to borrowers; it '
             'is the lender who receives those more valuable dollars.']},
    # id 297
    {'ch': 9,
     'q': 'A classmate says: "If market interest rates fall next year, I should sell my bonds now, '
          'because their prices will drop." What is wrong with this reasoning?',
     'opts': ['Falling interest rates raise the prices of previously issued bonds',
              'Falling interest rates lower the fixed rate paid on existing bonds',
              "Bond prices depend on the issuer's profits rather than interest rates",
              "Lower interest rates raise inflation, which cuts bonds' real value"],
     'exp': 'Bonds pay the rate fixed when they were issued. If market rates fall, older bonds with '
            'higher fixed payments become more attractive, so their prices rise rather than drop.',
     'why': [None,
             "A bond's interest rate is fixed when it is issued, so existing bondholders keep "
             'receiving the same rate when market rates fall.',
             'Bond prices respond to market interest rates: falling rates raise the prices of existing '
             'bonds, and rising rates lower them.',
             "This does not address the classmate's error, which is reversing the link: lower market "
             'rates make existing higher-rate bonds more valuable.']},
    # id 298
    {'ch': 9,
     'q': 'In a year, a country with a market-determined exchange rate imports $900 billion of goods '
          'and services and exports $700 billion. Its residents invest $150 billion abroad. How much '
          'capital flowed into the country from foreigners?',
     'opts': ['$350 billion', '$50 billion', '$200 billion', '$1,050 billion'],
     'exp': 'Imports − exports = capital inflow − capital outflow, so $900 − $700 = $200 billion = '
            'inflow − $150 billion. Capital inflow is $200 + $150 = $350 billion.',
     'why': [None,
             'This subtracts the $150 billion outflow from the $200 billion gap instead of adding it. '
             'The inflow must cover both the trade deficit and the outflow.',
             '$200 billion is the trade deficit, which equals **net** capital inflow. The gross inflow '
             'must also cover the $150 billion residents sent abroad.',
             'This adds imports and capital outflow, the total demand for foreign currency, but '
             'forgets to subtract exports: $1,050 − $700 = $350 billion.']},
    # id 299
    {'ch': 9,
     'q': 'Last year one euro cost $1.20. This year one euro costs $1.05. What happened to the dollar, '
          'and how will U.S. net exports tend to respond?',
     'opts': ['The dollar appreciated, so U.S. net exports tend to fall',
              'The dollar depreciated, so U.S. net exports tend to rise',
              'The dollar appreciated, so U.S. net exports tend to rise',
              'The dollar depreciated, so U.S. net exports tend to fall'],
     'exp': 'A euro now costs fewer dollars, so the dollar has appreciated. A stronger dollar makes '
            'imports cheaper for Americans and U.S. goods pricier abroad, so U.S. net exports tend to '
            'fall.',
     'why': [None,
             'The number that fell is the dollar price of a euro. Needing fewer dollars per euro means '
             'a stronger dollar, and that lowers net exports.',
             'Appreciation is right, but a stronger dollar makes U.S. exports more expensive for '
             'foreigners and imports cheaper, so net exports fall.',
             'Needing fewer dollars to buy a euro means the dollar appreciated, not depreciated; a '
             'depreciation would tend to raise net exports.']},
    # id 300
    {'ch': 9,
     'q': 'A classmate argues: "Since firms expand output when the price level rises unexpectedly, '
          'steady inflation can keep output above full employment indefinitely." What is the flaw?',
     'opts': ['Once contracts adjust to the higher prices, profit margins shrink and output returns to '
              'YF',
              'Firms reduce output when the price level rises, because their costs rise right away',
              'A higher price level shifts LRAS to the left, so output falls below full employment',
              'Output cannot exceed YF even briefly, since the LRAS curve is a vertical line'],
     'exp': 'A surprise rise in the price level raises output only because contracted costs lag behind '
            'product prices. Once contracts adjust, resource prices catch up, margins return to '
            'normal, and output moves back to YF.',
     'why': [None,
             'In the short run, costs are fixed by contracts and do not rise right away, which is why '
             'an unexpected rise in the price level expands output at first.',
             'The price level does not shift LRAS; LRAS depends on resources, technology, and '
             'institutions. The flaw is that output above YF cannot be sustained.',
             'Output can exceed YF temporarily after an unexpected rise in the price level. It just '
             'cannot stay there once contracts adjust.']},
    # id 301
    {'ch': 9,
     'q': 'Two countries each run trade deficits of the same size. Country A uses the net capital '
          'inflow to build factories and modern ports. Country B uses it to finance government budget '
          'deficits that support current consumption. Which comparison is most accurate?',
     'opts': ["A's borrowing is likely to raise future income, while B's is likely to lower it",
              'Both face lower future income, because a trade deficit drains national wealth',
              'B gains more, because consumption spending adds to GDP faster than investment',
              'Both gain equally, because the size of their capital inflows is the same'],
     'exp': 'Whether a trade deficit is harmful depends on how the borrowed capital is used. '
            'Productive investment raises future productivity and income, while borrowing to fund '
            'current consumption reduces capital formation and future income.',
     'why': [None,
             'A trade deficit mirrors a net capital inflow and is not automatically a drain. When the '
             'funds go into productive investment, as in A, future income rises.',
             'Consumption adds to current spending but does not raise future productivity, so '
             'borrowing to fund it reduces future income.',
             'The size of the inflow is not what matters; the use of the funds is. Investment and '
             'consumption have very different effects on future income.']},
    # id 302
    {'ch': 9,
     'q': "This year's price level turns out higher than buyers and sellers anticipated when they "
          'signed their wage contracts. In the short run, which set of outcomes is most likely?',
     'opts': ['Real wages fall, employment rises, and unemployment drops below the natural rate',
              'Real wages rise, employment falls, and unemployment climbs above the natural rate',
              'Real wages fall, employment falls, and unemployment climbs above the natural rate',
              'Real wages are unchanged, because nominal wages rise with the price level at once'],
     'exp': 'Nominal wages are fixed by contracts, so a surprise rise in the price level lowers real '
            'wages and widens profit margins. Firms expand output and hiring, pushing unemployment '
            'below the natural rate for a time.',
     'why': [None,
             'With nominal wages fixed, higher prices lower real wages rather than raise them, so '
             'labor becomes cheaper relative to output and firms hire more.',
             'Lower real wages make hiring more profitable, so employment rises. Unemployment above '
             'the natural rate goes with a price level **below** what was expected.',
             'Wages are set by prior contracts, so they cannot jump at once. That lag is exactly what '
             'makes real wages fall in the short run.']},
    # id 303
    {'ch': 9,
     'q': 'The price level falls. Households and firms now need less money for their purchases, so '
          'they lend out more, the real interest rate declines, and firms borrow to buy new equipment. '
          'This chain explains which feature of the AD–AS model?',
     'opts': ['Why the aggregate demand curve slopes downward',
              'Why the short-run aggregate supply curve slopes up',
              'Why the aggregate demand curve shifts to the right',
              'Why the long-run aggregate supply curve is vertical'],
     'exp': 'A lower price level reduces money demand and lowers the real interest rate, which '
            'stimulates purchases. That is one of the three reasons AD slopes downward: a movement '
            'along a given AD curve, not a shift.',
     'why': [None,
             'SRAS concerns what firms supply as prices change relative to contracted costs. This '
             'chain is about buyers purchasing more, which is the demand side.',
             'A lower real interest rate shifts AD only when something other than the price level '
             'causes it. Here the price level started the chain, so the economy moves along AD.',
             'LRAS reflects resources, technology, and institutions, which this chain never touches. '
             'The chain describes how purchases respond to the price level.'],
     'expFig': {'type': 'graph',
                'x': 'Real GDP',
                'y': 'Price level',
                'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD1'}],
                'points': [{'at': [35, 65], 'label': 'A'}, {'at': [60, 40], 'label': 'B'}],
                'guides': True,
                'xticks': [[35, 'Y1'], [60, 'Y2']],
                'yticks': [[40, 'P2'], [65, 'P1']],
                'arrows': [{'from': [40, 64], 'to': [54, 50]}],
                'alt': 'A single AD1 curve. When the price level falls from P1 to P2, the economy '
                       'moves down along AD1 from point A to point B, and output rises from Y1 to Y2. '
                       'An arrow runs along the curve from A toward B; the curve itself does not '
                       'move.'}},
    # id 304
    {'ch': 9,
     'q': 'In Country A, investment opportunities are weak, so domestic demand for loanable funds is '
          'low and its real interest rate is below rates abroad. In Country B, strong investment '
          'demand has pushed the real interest rate above rates abroad. In a global loanable funds '
          'market, which capital flows are expected?',
     'opts': ['Capital flows out of A and into B, seeking the higher expected rate of return',
              "Capital flows into A and out of B, since A's low rates make its borrowing cheap",
              "Capital flows out of both, because each country's real rate differs from abroad",
              "Capital flows out of B and into A, since B's high real rates signal greater risk"],
     'exp': "Capital moves toward markets where the expected rate of return is higher. A's weak demand "
            "and low real rate lead to a capital outflow, while B's strong demand and high real rate "
            'attract an inflow.',
     'why': [None,
             'Cheap borrowing does not attract lenders. Lenders supply the capital, and they send it '
             'where returns are higher, which is B, not A.',
             'The gaps point in opposite directions: a rate below world rates pushes capital out, but '
             'a rate above world rates pulls capital in.',
             'In this model a high real rate from strong demand for loanable funds attracts capital '
             'rather than signaling risk, so funds flow toward B.'],
     'fig': {'type': 'graph',
             'x': 'Quantity of loanable funds',
             'y': 'Real interest rate',
             'lines': [{'pts': [[15, 15], [85, 85]], 'cls': 's', 'label': 'S'},
                       {'pts': [[10, 50], [50, 10]], 'cls': 'd', 'label': 'D1'},
                       {'pts': [[32, 88], [88, 32]], 'cls': 'd', 'label': 'D2'},
                       {'pts': [[8, 48], [95, 48]], 'cls': 'm', 'label': 'rw'}],
             'points': [{'at': [30, 30], 'label': 'e1'}, {'at': [60, 60], 'label': 'e2'}],
             'guides': True,
             'yticks': [[30, 'r1'], [48, 'rw'], [60, 'r2']],
             'alt': 'A domestic loanable funds market with supply S. Weak domestic demand D1, like '
                    "Country A's, crosses S at e1 at the real interest rate r1. Strong domestic demand "
                    "D2, like Country B's, crosses S at e2 at the real interest rate r2. A horizontal "
                    'line marks the world real interest rate rw, which lies between r1 and r2.'}},
    # id 305
    {'ch': 10,
     'q': 'The economy starts at E1. Which event could cause the change shown in the graph?',
     'opts': ["A surge in stock prices that raises households' real wealth",
              'A rise in the real interest rate that makes borrowing costlier',
              'A technological advance that raises productivity across firms',
              "A drop in resource prices that lowers firms' production costs"],
     'exp': 'The graph shows AD shifting right while SRAS and LRAS stay put. A stock market surge '
            "raises households' real wealth, and an increase in real wealth shifts AD to the right.",
     'why': [None,
             'A higher real interest rate does shift AD, but to the left. The graph shows AD moving to '
             'the right.',
             'A technology gain would shift LRAS and SRAS to the right, but in the graph only AD '
             'moves.',
             'Lower resource prices would also raise output, but they shift SRAS to the right. In the '
             'graph SRAS stays put and AD moves.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'm', 'label': 'AD1'},
                       {'pts': [[35, 85], [95, 25]], 'cls': 'd', 'label': 'AD2', 'dash': True},
                       {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS'},
                       {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
             'points': [{'at': [50, 50], 'label': 'E1'}, {'at': [60, 60], 'label': 'E2'}],
             'guides': True,
             'xticks': [[50, 'YF'], [60, 'Y2']],
             'yticks': [[50, 'P1'], [60, 'P2']],
             'arrows': [{'from': [72, 30], 'to': [87, 30]}],
             'alt': 'AD1 and SRAS cross at E1 on the vertical LRAS line at YF and price level P1. A '
                    'second curve, AD2, lies to the right of AD1 and crosses SRAS at E2, at output Y2 '
                    'and the higher price level P2. An arrow points from AD1 toward AD2.'}},
    # id 306
    {'ch': 10,
     'q': 'An unanticipated increase in aggregate demand moves the economy from A to B. If policy does '
          'not change, where does the economy settle in the long run, and why?',
     'opts': ['At C, as rising resource prices shift SRAS to the left',
              'At B, as the stronger demand keeps output at Y2 for good',
              'At A, as buyers adjust and AD shifts back to its old position',
              'Beyond Y2, as LRAS shifts right to meet the higher AD2'],
     'exp': 'At B, output exceeds YF and resource markets are tight. As contracts expire, resource '
            'prices rise and shift SRAS left until it crosses AD2 at C, with output back at YF and a '
            'higher price level.',
     'why': [None,
             'Output at B is above YF only because contracted costs lag behind product prices. Once '
             'resource prices catch up, output cannot stay at Y2.',
             'Nothing makes buyers reverse the increase in AD. The adjustment comes through SRAS as '
             'resource prices rise, so the price level ends above its level at A.',
             'Higher demand does not add resources, technology, or better institutions, so LRAS stays '
             'at YF and output returns there.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'm', 'label': 'AD1'},
                       {'pts': [[35, 85], [95, 25]], 'cls': 'd', 'label': 'AD2'},
                       {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS1'},
                       {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
             'points': [{'at': [50, 50], 'label': 'A'},
                        {'at': [60, 60], 'label': 'B'},
                        {'at': [50, 70], 'label': 'C'}],
             'guides': True,
             'xticks': [[50, 'YF'], [60, 'Y2']],
             'yticks': [[50, 'P1'], [60, 'P2'], [70, 'P3']],
             'alt': 'AD1 and SRAS1 cross at point A on the vertical LRAS line at YF and price level '
                    'P1. AD2, to the right of AD1, crosses SRAS1 at point B at output Y2 and price '
                    'level P2. Point C lies on AD2 directly above A on the LRAS line, at price level '
                    'P3.'},
     'expFig': {'type': 'graph',
                'x': 'Real GDP',
                'y': 'Price level',
                'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'm', 'label': 'AD1'},
                          {'pts': [[35, 85], [95, 25]], 'cls': 'd', 'label': 'AD2'},
                          {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS1'},
                          {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'},
                          {'pts': [[10, 30], [70, 90]], 'cls': 's', 'label': 'SRAS2', 'dash': True}],
                'points': [{'at': [50, 50], 'label': 'A'},
                           {'at': [60, 60], 'label': 'B'},
                           {'at': [50, 70], 'label': 'C'}],
                'guides': True,
                'xticks': [[50, 'YF'], [60, 'Y2']],
                'yticks': [[50, 'P1'], [60, 'P2'], [70, 'P3']],
                'arrows': [{'from': [74, 76], 'to': [58, 76]}],
                'alt': 'Same graph with a new curve SRAS2, to the left of SRAS1, crossing AD2 at point '
                       'C on the LRAS line at price level P3. An arrow points from SRAS1 toward '
                       'SRAS2.'}},
    # id 307
    {'ch': 10,
     'q': 'After an unanticipated shift from AD1 to AD2, the economy is at E2. Which statement '
          'correctly describes E2 and what happens next if policy does not change?',
     'opts': ['Unemployment exceeds the natural rate; falling resource prices and real interest rates '
              'gradually restore YF',
              'Unemployment is below the natural rate; falling resource prices and real interest rates '
              'gradually restore YF',
              'Unemployment exceeds the natural rate; rising resource prices shift SRAS to the left '
              'and restore YF',
              'Output Y2 becomes the new full-employment level, since LRAS shifts left to follow AD2'],
     'exp': 'At E2, output is below YF, so unemployment is above the natural rate. Weak demand '
            'gradually lowers resource prices, shifting SRAS right, and lower real interest rates '
            'support AD, returning output to YF at a lower price level.',
     'why': [None,
             'The adjustment is right, but E2 is misread: output Y2 is below YF, so unemployment is '
             '**above** the natural rate, not below it.',
             'Rising resource prices are the adjustment after a boom. In a slump, weak demand for '
             'resources pushes their prices down, shifting SRAS to the right.',
             'A drop in AD does not change resources, technology, or institutions, so LRAS stays at YF '
             'and the economy eventually returns there.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'm', 'label': 'AD1'},
                       {'pts': [[8, 72], [68, 12]], 'cls': 'd', 'label': 'AD2', 'dash': True},
                       {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS1'},
                       {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
             'points': [{'at': [50, 50], 'label': 'E1'}, {'at': [40, 40], 'label': 'E2'}],
             'guides': True,
             'xticks': [[40, 'Y2'], [50, 'YF']],
             'yticks': [[40, 'P2'], [50, 'P1']],
             'alt': 'AD1 and SRAS1 cross at E1 on the vertical LRAS line at YF and price level P1. '
                    'AD2, to the left of AD1, crosses SRAS1 at E2 at the lower output Y2 and lower '
                    'price level P2.'},
     'expFig': {'type': 'graph',
                'x': 'Real GDP',
                'y': 'Price level',
                'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'm', 'label': 'AD1'},
                          {'pts': [[8, 72], [68, 12]], 'cls': 'd', 'label': 'AD2', 'dash': True},
                          {'pts': [[20, 20], [85, 85]], 'cls': 'm', 'label': 'SRAS1'},
                          {'pts': [[30, 10], [95, 75]], 'cls': 's', 'label': 'SRAS2', 'dash': True},
                          {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
                'points': [{'at': [50, 50], 'label': 'E1'},
                           {'at': [40, 40], 'label': 'E2'},
                           {'at': [50, 30], 'label': 'E3'}],
                'guides': True,
                'xticks': [[40, 'Y2'], [50, 'YF']],
                'yticks': [[30, 'P3'], [40, 'P2'], [50, 'P1']],
                'arrows': [{'from': [72, 70], 'to': [86, 70]}],
                'alt': 'Same graph with SRAS2, to the right of SRAS1, crossing AD2 at E3 on the LRAS '
                       'line at YF and the even lower price level P3.'}},
    # id 308
    {'ch': 10,
     'q': 'A crop failure raises resource prices and moves the economy from E1 to E2. If the crop '
          'failure turns out to be temporary, what is the long-run outcome?',
     'opts': ['Resource prices fall back, SRAS returns to SRAS1, and the economy returns to E1',
              "LRAS shifts left to Y2, and E2 becomes the economy's new long-run equilibrium",
              'The price level stays at P2 while output alone recovers to the YF output rate',
              'AD shifts left to bring the price level back down to P1 at the lower output rate Y2'],
     'exp': 'Because the shock is temporary, resource prices eventually fall back, SRAS returns to '
            'SRAS1, and the economy returns to E1 with output at YF and price level P1.',
     'why': [None,
             'LRAS shifts left only if the adverse supply shock is **permanent**. A temporary crop '
             'failure leaves long-run capacity unchanged.',
             'Output can recover only as SRAS shifts back, and that movement down along AD brings the '
             'price level back to P1 as well.',
             'Nothing reduces AD here. Recovery comes from supply as resource prices fall, and a '
             'decrease in AD would cut output even further.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD'},
                       {'pts': [[20, 20], [85, 85]], 'cls': 'm', 'label': 'SRAS1'},
                       {'pts': [[10, 30], [70, 90]], 'cls': 's', 'label': 'SRAS2', 'dash': True},
                       {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
             'points': [{'at': [50, 50], 'label': 'E1'}, {'at': [40, 60], 'label': 'E2'}],
             'guides': True,
             'xticks': [[40, 'Y2'], [50, 'YF']],
             'yticks': [[50, 'P1'], [60, 'P2']],
             'alt': 'AD crosses SRAS1 at E1 on the vertical LRAS line at YF and price level P1. SRAS2, '
                    'to the left of SRAS1, crosses AD at E2 at the lower output Y2 and the higher '
                    'price level P2.'}},
    # id 309
    {'ch': 10,
     'q': 'The graph shows LRAS1 shifting to LRAS2 and SRAS1 shifting to SRAS2. Which event could '
          'cause both shifts?',
     'opts': ["Capital formation that enlarges the economy's stock of machines",
              'An unusually favorable growing season that yields a bumper crop',
              'A reduction in the expected rate of inflation built into contracts',
              'A temporary drop in the world price of a key imported resource'],
     'exp': "Capital formation increases the supply of resources, which raises the economy's "
            'sustainable output and shifts LRAS to the right; an LRAS shift moves SRAS in the same '
            'direction.',
     'why': [None,
             'Favorable weather is a temporary supply shock. It shifts only SRAS, because one good '
             'harvest cannot be counted on in the future.',
             'Lower expected inflation increases SRAS, but it does not change resources, technology, '
             'or institutions, so LRAS would not move.',
             "A temporary drop in an import's price is a favorable supply shock that shifts SRAS but "
             'leaves long-run capacity unchanged.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD'},
                       {'pts': [[20, 20], [85, 85]], 'cls': 'm', 'label': 'SRAS1'},
                       {'pts': [[36, 12], [95, 71]], 'cls': 's', 'label': 'SRAS2', 'dash': True},
                       {'pts': [[50, 8], [50, 92]], 'cls': 'm', 'label': 'LRAS1'},
                       {'pts': [[62, 8], [62, 80]], 'cls': 'v', 'label': 'LRAS2', 'dash': True}],
             'points': [{'at': [50, 50], 'label': 'E1'}, {'at': [62, 38], 'label': 'E2'}],
             'guides': True,
             'xticks': [[50, 'YF1'], [62, 'YF2']],
             'yticks': [[38, 'P2'], [50, 'P1']],
             'arrows': [{'from': [52, 70], 'to': [60, 70]}, {'from': [63, 58], 'to': [80, 58]}],
             'alt': 'AD crosses SRAS1 at E1 on the vertical line LRAS1 at output YF1 and price level '
                    'P1. A second vertical line, LRAS2, stands at the larger output YF2, and SRAS2 '
                    'lies to the right of SRAS1. AD crosses SRAS2 at E2 on LRAS2, at output YF2 and '
                    'the lower price level P2. Arrows point from LRAS1 toward LRAS2 and from SRAS1 '
                    'toward SRAS2.'}},
    # id 310
    {'ch': 10,
     'q': 'The economy moves from E1 to E2 in the graph. Which event fits this change?',
     'opts': ['An unexpected fall in the world price of a key imported resource',
              'A lasting improvement in technology that raises productivity',
              'An increase in the expected rate of inflation among most businesses',
              'A depreciation of the dollar that raises U.S. net exports'],
     'exp': 'Only SRAS shifts right while AD and LRAS stay put, which is a favorable supply shock. An '
            'unexpected fall in the price of a key imported resource lowers costs, so output '
            'temporarily exceeds YF and the price level falls.',
     'why': [None,
             'A lasting technology improvement would shift LRAS to the right along with SRAS, but in '
             'the graph LRAS stays at YF.',
             'Higher expected inflation decreases SRAS, shifting it to the left, while the graph shows '
             'SRAS shifting to the right.',
             'A weaker dollar raises net exports and shifts AD, but in the graph AD is unchanged and '
             'only SRAS moves.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD'},
                       {'pts': [[20, 20], [85, 85]], 'cls': 'm', 'label': 'SRAS1'},
                       {'pts': [[30, 10], [95, 75]], 'cls': 's', 'label': 'SRAS2', 'dash': True},
                       {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
             'points': [{'at': [50, 50], 'label': 'E1'}, {'at': [60, 40], 'label': 'E2'}],
             'guides': True,
             'xticks': [[50, 'YF'], [60, 'Y2']],
             'yticks': [[40, 'P2'], [50, 'P1']],
             'alt': 'AD crosses SRAS1 at E1 on the vertical LRAS line at YF and price level P1. SRAS2, '
                    'to the right of SRAS1, crosses AD at E2 at the higher output Y2 and the lower '
                    'price level P2.'}},
    # id 311
    {'ch': 10,
     'q': 'Suppose businesses and consumers come to expect a higher rate of inflation. Statement I: '
          'This tends to increase aggregate demand. Statement II: This tends to decrease short-run '
          'aggregate supply.',
     'opts': ['Both Statement I and Statement II are true',
              'Statement I is true and Statement II is false',
              'Statement I is false and Statement II is true',
              'Both Statement I and Statement II are false'],
     'exp': 'An increase in expected inflation is one of the factors that shift AD outward, so '
            'Statement I is true. Because lower expected inflation increases SRAS, higher expected '
            'inflation decreases it, so Statement II is true as well.',
     'why': [None,
             'Statement II is also true: expected inflation is an SRAS shifter, and an increase in it '
             'decreases SRAS.',
             'Statement I is also true: an increase in the expected rate of inflation is on the list '
             'of factors that shift AD outward.',
             'Both statements are true. Higher expected inflation increases AD and decreases SRAS, and '
             'together these push up the price level.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD1'},
                       {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS1'},
                       {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
             'points': [{'at': [50, 50], 'label': 'E1'}],
             'guides': True,
             'xticks': [[50, 'YF']],
             'yticks': [[50, 'P1']],
             'alt': "The economy's starting position: a downward-sloping AD1 curve, an upward-sloping "
                    'SRAS1 curve, and a vertical LRAS line all pass through E1 at full-employment '
                    'output YF and price level P1. No curve has shifted yet.'},
     'expFig': {'type': 'graph',
                'x': 'Real GDP',
                'y': 'Price level',
                'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'm', 'label': 'AD1'},
                          {'pts': [[35, 85], [95, 25]], 'cls': 'd', 'label': 'AD2', 'dash': True},
                          {'pts': [[20, 20], [85, 85]], 'cls': 'm', 'label': 'SRAS1'},
                          {'pts': [[10, 30], [70, 90]], 'cls': 's', 'label': 'SRAS2', 'dash': True},
                          {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
                'points': [{'at': [50, 50], 'label': 'E1'}, {'at': [50, 70], 'label': 'E2'}],
                'guides': True,
                'xticks': [[50, 'YF']],
                'yticks': [[50, 'P1'], [70, 'P2']],
                'arrows': [{'from': [72, 30], 'to': [87, 30]}, {'from': [74, 76], 'to': [58, 76]}],
                'alt': 'After the change: AD1 shifts right to AD2 and SRAS1 shifts left to SRAS2. The '
                       'two shifts are drawn the same size, so the new intersection E2 lies directly '
                       'above E1 at the higher price level P2; with different-sized shifts output '
                       'could end above or below YF.'}},
    # id 312
    {'ch': 10,
     'q': 'A classmate says: "A deep recession in Europe will shift the U.S. SRAS curve to the left, '
          'because European firms will make fewer goods for us." Which correction best fits the AD–AS '
          'model?',
     'opts': ['Lower real incomes abroad reduce demand for U.S. exports, shifting U.S. AD left',
              'Lower real incomes abroad raise demand for U.S. exports, shifting U.S. AD right',
              'Lower real incomes abroad lower U.S. resource prices, shifting U.S. SRAS right',
              'Lower real incomes abroad shrink U.S. potential output, shifting U.S. LRAS left'],
     'exp': "Real incomes abroad are an AD shifter. When foreigners' incomes fall, they buy fewer U.S. "
            'exports, so U.S. aggregate demand decreases; nothing has changed U.S. resource prices, '
            'expected inflation, or supply conditions.',
     'why': [None,
             'Lower incomes abroad mean foreigners buy less of everything, including U.S. exports, so '
             'U.S. AD falls rather than rises.',
             'The event reaches the U.S. through demand for its exports, an AD shifter. It does not '
             'directly change U.S. resource prices, so SRAS is not the curve that moves.',
             'U.S. potential output depends on U.S. resources, technology, and institutions, none of '
             'which a European recession changes.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD1'},
                       {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS1'},
                       {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
             'points': [{'at': [50, 50], 'label': 'E1'}],
             'guides': True,
             'xticks': [[50, 'YF']],
             'yticks': [[50, 'P1']],
             'alt': "The economy's starting position: a downward-sloping AD1 curve, an upward-sloping "
                    'SRAS1 curve, and a vertical LRAS line all pass through E1 at full-employment '
                    'output YF and price level P1. No curve has shifted yet.'},
     'expFig': {'type': 'graph',
                'x': 'Real GDP',
                'y': 'Price level',
                'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'm', 'label': 'AD1'},
                          {'pts': [[8, 72], [68, 12]], 'cls': 'd', 'label': 'AD2', 'dash': True},
                          {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS1'},
                          {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
                'points': [{'at': [50, 50], 'label': 'E1'}, {'at': [40, 40], 'label': 'E2'}],
                'guides': True,
                'xticks': [[40, 'Y2'], [50, 'YF']],
                'yticks': [[40, 'P2'], [50, 'P1']],
                'arrows': [{'from': [68, 30], 'to': [52, 30]}],
                'alt': 'After the change: AD1 shifts left to AD2 while SRAS1 and LRAS stay put. AD2 '
                       'crosses SRAS1 at E2, at output Y2 below YF and the lower price level P2. An '
                       'arrow points from AD1 toward AD2.'}},
    # id 313
    {'ch': 10,
     'q': 'Which pair of events could **each** produce an unsustainable boom with output above YF?',
     'opts': ['A surprise jump in consumer optimism and an unexpected drop in oil prices',
              'A surprise jump in consumer optimism and an unexpected surge in oil prices',
              'Steady, anticipated capital growth and an unexpected surge in oil prices',
              'A surprise rise in real interest rates and an unexpected drop in oil prices'],
     'exp': 'Booms come from unanticipated increases in AD, such as a surge in consumer optimism, and '
            'from favorable supply shocks, such as an unexpected drop in oil prices. Each can '
            'temporarily push output above YF.',
     'why': [None,
             'Optimism fits, but an unexpected surge in oil prices is an unfavorable supply shock that '
             'causes recessions, not booms.',
             'Anticipated capital growth raises sustainable output without creating a boom, and an oil '
             'price surge is an unfavorable supply shock.',
             'The oil price drop fits, but a surprise rise in real interest rates reduces AD, which '
             'pushes output below YF.']},
    # id 314
    {'ch': 10,
     'q': 'An economy is in an unsustainable boom with unemployment below the natural rate. According '
          'to the AD–AS model, which two forces will help bring it back to long-run equilibrium?',
     'opts': ['Rising real resource prices and rising real interest rates',
              'Falling real resource prices and falling real interest rates',
              'Rising real resource prices and falling real interest rates',
              'Rising real resource prices and an outward shift of LRAS'],
     'exp': 'During a boom, strong demand for resources pushes real resource prices up, shifting SRAS '
            'left, and strong investment demand raises real interest rates, which retards AD. Both '
            'forces pull output back toward YF.',
     'why': [None,
             'Falling real resource prices and falling real interest rates are the forces at work in a '
             '**recession**, when demand for resources and investment is weak.',
             'Rising resource prices fit, but in a boom strong investment demand pushes real interest '
             'rates up, not down, and higher rates retard AD.',
             'A boom does not change resources, technology, or institutions, so LRAS does not shift. '
             'The second force is rising real interest rates.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[35, 85], [95, 25]], 'cls': 'd', 'label': 'AD1'},
                       {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS1'},
                       {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
             'points': [{'at': [60, 60], 'label': 'B'}],
             'guides': True,
             'xticks': [[50, 'YF'], [60, 'Y1']],
             'yticks': [[60, 'P1']],
             'alt': "The economy's current position: AD1 crosses SRAS1 at point B, at output Y1 and "
                    'price level P1. The vertical LRAS line stands at YF, to the left of Y1. No curve '
                    'has shifted yet.'},
     'expFig': {'type': 'graph',
                'x': 'Real GDP',
                'y': 'Price level',
                'lines': [{'pts': [[35, 85], [95, 25]], 'cls': 'm', 'label': 'AD1'},
                          {'pts': [[31, 85], [81, 35]], 'cls': 'd', 'label': 'AD2', 'dash': True},
                          {'pts': [[20, 20], [85, 85]], 'cls': 'm', 'label': 'SRAS1'},
                          {'pts': [[8, 24], [69, 85]], 'cls': 's', 'label': 'SRAS2', 'dash': True},
                          {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
                'points': [{'at': [60, 60], 'label': 'B'}, {'at': [50, 66], 'label': 'C'}],
                'guides': True,
                'xticks': [[50, 'YF'], [60, 'Y1']],
                'yticks': [[60, 'P1'], [66, 'P2']],
                'arrows': [{'from': [74, 76], 'to': [62, 76]}, {'from': [83, 38], 'to': [78, 38]}],
                'alt': 'After adjustment: SRAS1 shifts left to SRAS2 as real resource prices rise, and '
                       'AD1 shifts slightly left to AD2 as real interest rates rise. AD2 and SRAS2 '
                       'cross at point C on the LRAS line at YF and the higher price level P2. Arrows '
                       'point from the original curves toward the new ones.'}},
    # id 315
    {'ch': 10,
     'q': 'A war permanently cuts off a major supply source of a key imported resource, raising its '
          'world price. How does the long-run outcome differ from that of a temporary shock of the '
          'same size?',
     'opts': ['LRAS shifts left, so the lower output rate becomes the new full-employment level',
              'SRAS shifts back to its original position, so output returns to the original YF',
              'AD shifts left to offset the higher costs, so the price level returns to its start',
              'LRAS shifts right as firms invest in substitutes, so output ends above the old YF'],
     'exp': "A permanent adverse supply shock shrinks the economy's productive potential: LRAS shifts "
            'left, and the reduced output rate becomes the new full-employment level.',
     'why': [None,
             'SRAS returning to its original position is the outcome of a **temporary** shock, when '
             'resource prices eventually fall back. A permanent shock lowers potential output.',
             'Nothing in the shock reduces AD, and a leftward AD shift would lower output even further '
             'rather than offset the higher costs.',
             'Permanently losing a source of a key resource reduces the supply of resources, which '
             'shifts LRAS to the left, not the right.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD1'},
                       {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS1'},
                       {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
             'points': [{'at': [50, 50], 'label': 'E1'}],
             'guides': True,
             'xticks': [[50, 'YF']],
             'yticks': [[50, 'P1']],
             'alt': "The economy's starting position: a downward-sloping AD1 curve, an upward-sloping "
                    'SRAS1 curve, and a vertical LRAS line all pass through E1 at full-employment '
                    'output YF and price level P1. No curve has shifted yet.'},
     'expFig': {'type': 'graph',
                'x': 'Real GDP',
                'y': 'Price level',
                'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD1'},
                          {'pts': [[20, 20], [85, 85]], 'cls': 'm', 'label': 'SRAS1'},
                          {'pts': [[10, 30], [70, 90]], 'cls': 's', 'label': 'SRAS2', 'dash': True},
                          {'pts': [[50, 8], [50, 92]], 'cls': 'm', 'label': 'LRAS1'},
                          {'pts': [[40, 8], [40, 78]], 'cls': 'v', 'label': 'LRAS2', 'dash': True}],
                'points': [{'at': [50, 50], 'label': 'E1'}, {'at': [40, 60], 'label': 'E2'}],
                'guides': True,
                'xticks': [[40, 'YF2'], [50, 'YF1']],
                'yticks': [[50, 'P1'], [60, 'P2']],
                'arrows': [{'from': [74, 76], 'to': [58, 76]}, {'from': [48, 20], 'to': [42, 20]}],
                'alt': 'After the change: SRAS1 shifts left to SRAS2 and LRAS shifts left from LRAS1 '
                       'at YF1 to LRAS2 at YF2. AD1 crosses SRAS2 at E2, which lies on LRAS2 at the '
                       'higher price level P2. Arrows point from the original curves toward the new '
                       'ones.'}},
    # id 316
    {'ch': 10,
     'q': 'Statement I: Falling energy prices in 2007 and early 2008 increased SRAS and softened the '
          '2008–2009 recession. Statement II: Falling housing prices after mid-2006 raised mortgage '
          'defaults and foreclosures, which reduced AD.',
     'opts': ['Statement I is false and Statement II is true',
              'Statement I is true and Statement II is false',
              'Both Statement I and Statement II are true',
              'Both Statement I and Statement II are false'],
     'exp': 'Energy prices soared, not fell, during 2007 and early 2008, an unanticipated reduction in '
            'SRAS that deepened the downturn, so Statement I is false. Statement II is true: falling '
            'housing prices raised defaults and foreclosures and reduced AD.',
     'why': [None,
             'Both judgments are reversed. Energy prices soared in 2007–2008, reducing SRAS, and '
             'falling housing prices after mid-2006 did reduce AD.',
             'Statement I is false: energy prices soared rather than fell, so the energy shock reduced '
             'SRAS and made the recession worse.',
             'Statement II is true: from the second half of 2006, falling housing prices raised '
             'mortgage defaults and foreclosures, which reduced AD.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD1'},
                       {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS1'},
                       {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
             'points': [{'at': [50, 50], 'label': 'E1'}],
             'guides': True,
             'xticks': [[50, 'YF']],
             'yticks': [[50, 'P1']],
             'alt': "The economy's starting position: a downward-sloping AD1 curve, an upward-sloping "
                    'SRAS1 curve, and a vertical LRAS line all pass through E1 at full-employment '
                    'output YF and price level P1. No curve has shifted yet.'},
     'expFig': {'type': 'graph',
                'x': 'Real GDP',
                'y': 'Price level',
                'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'm', 'label': 'AD1'},
                          {'pts': [[8, 72], [68, 12]], 'cls': 'd', 'label': 'AD2', 'dash': True},
                          {'pts': [[20, 20], [85, 85]], 'cls': 'm', 'label': 'SRAS1'},
                          {'pts': [[8, 18], [70, 80]], 'cls': 's', 'label': 'SRAS2', 'dash': True},
                          {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
                'points': [{'at': [50, 50], 'label': 'E1'}, {'at': [35, 45], 'label': 'E2'}],
                'guides': True,
                'xticks': [[35, 'Y2'], [50, 'YF']],
                'yticks': [[45, 'P2'], [50, 'P1']],
                'arrows': [{'from': [68, 30], 'to': [52, 30]}, {'from': [75, 76], 'to': [67, 76]}],
                'alt': 'After the events: AD1 shifts left to AD2 and SRAS1 shifts left to SRAS2, while '
                       'LRAS stays put. AD2 and SRAS2 cross at E2, at output Y2 well below YF and '
                       'price level P2. Arrows point from the original curves toward the new ones.'}},
    # id 317
    {'ch': 10,
     'q': "Economy A's output grows steadily each year from predictable capital formation. Economy B's "
          "output jumps when an unexpected surge in spending raises AD. Why does A's growth not "
          "disrupt macroeconomic equilibrium while B's expansion does?",
     'opts': ["A's growth is anticipated and shifts LRAS, while B's surprise pushes output beyond YF",
              "A's growth shifts SRAS but not LRAS, while B's rise in AD shifts both of them",
              "A's growth raises prices in both markets, while B's leaves the overall price level "
              'unchanged',
              "A's growth is unanticipated and shifts AD, while B's surprise shifts LRAS outward"],
     'exp': "Steady, predictable growth shifts LRAS and SRAS right and is built into people's plans, "
            'so the higher output is sustainable. An unanticipated rise in AD pushes output beyond YF '
            'only until resource prices catch up.',
     'why': [None,
             'Capital formation raises sustainable capacity, so it shifts LRAS as well as SRAS. A rise '
             'in AD shifts the demand curve, not either supply curve.',
             'An unanticipated rise in AD raises the price level. What separates the two cases is '
             "whether output stays within the economy's sustainable capacity.",
             "This swaps the two cases. A's predictable growth is anticipated and shifts LRAS, while "
             "B's surprise is a shift in AD."],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD1'},
                       {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS1'},
                       {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
             'points': [{'at': [50, 50], 'label': 'E1'}],
             'guides': True,
             'xticks': [[50, 'YF']],
             'yticks': [[50, 'P1']],
             'alt': "The economy's starting position: a downward-sloping AD1 curve, an upward-sloping "
                    'SRAS1 curve, and a vertical LRAS line all pass through E1 at full-employment '
                    'output YF and price level P1. No curve has shifted yet.'},
     'expFig': {'type': 'graph',
                'x': 'Real GDP',
                'y': 'Price level',
                'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'm', 'label': 'AD1'},
                          {'pts': [[27, 85], [80, 32]], 'cls': 'd', 'label': 'AD2', 'dash': True},
                          {'pts': [[20, 20], [85, 85]], 'cls': 'm', 'label': 'SRAS1'},
                          {'pts': [[32, 20], [82, 70]], 'cls': 's', 'label': 'SRAS2', 'dash': True},
                          {'pts': [[50, 8], [50, 92]], 'cls': 'm', 'label': 'LRAS1'},
                          {'pts': [[62, 8], [62, 80]], 'cls': 'v', 'label': 'LRAS2', 'dash': True}],
                'points': [{'at': [50, 50], 'label': 'E1'}, {'at': [62, 50], 'label': 'E2'}],
                'guides': True,
                'xticks': [[50, 'YF1'], [62, 'YF2']],
                'yticks': [[50, 'P1']],
                'arrows': [{'from': [52, 20], 'to': [60, 20]}],
                'alt': "Economy A's steady growth: LRAS shifts right from YF1 to YF2, SRAS shifts "
                       'right to SRAS2, and AD grows to AD2. The new equilibrium E2 lies on LRAS2 at '
                       'the larger output YF2 and the same price level as E1, so the higher output is '
                       'sustainable.'}},
    # id 318
    {'ch': 10,
     'q': 'A researcher notices that stock and housing prices typically climb before and during '
          'expansions and drop before and during recessions. How does the AD–AS model link these price '
          'movements to the business cycle?',
     'opts': ['Changes in household wealth shift AD, amplifying both expansions and downturns',
              "Changes in asset prices shift LRAS, altering the economy's long-run potential output",
              "Rising asset prices raise firms' costs, shifting SRAS to the left during expansions",
              'Asset prices trail output, so they react to business cycles but do not drive them'],
     'exp': 'Real wealth is an AD shifter. Rising stock and housing prices raise wealth and AD, and '
            'falling prices reduce wealth and AD, which amplifies both expansions and downturns.',
     'why': [None,
             'Asset prices do not change resources, technology, or institutions, so they do not shift '
             'LRAS. They work through household wealth and AD.',
             'Stock and housing prices are not production costs in the AD–AS model. They change '
             'household wealth, which shifts AD rather than SRAS.',
             'Asset prices generally move **before** and during expansions and recessions, and the '
             'large drop in housing prices helped make the 2008–2009 recession more severe.'],
     'expFig': {'type': 'graph',
                'x': 'Real GDP',
                'y': 'Price level',
                'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'm', 'label': 'AD0'},
                          {'pts': [[35, 85], [95, 25]], 'cls': 'd', 'label': 'AD1', 'dash': True},
                          {'pts': [[8, 72], [68, 12]], 'cls': 'd', 'label': 'AD2', 'dash': True},
                          {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS'},
                          {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
                'points': [{'at': [50, 50], 'label': 'E0'},
                           {'at': [60, 60], 'label': 'E1'},
                           {'at': [40, 40], 'label': 'E2'}],
                'guides': True,
                'xticks': [[40, 'Y2'], [50, 'YF'], [60, 'Y1']],
                'arrows': [{'from': [72, 30], 'to': [87, 30]}, {'from': [68, 30], 'to': [52, 30]}],
                'alt': 'Starting from AD0, rising stock and housing prices raise wealth and shift AD '
                       'right to AD1, moving the economy to E1 at higher output; falling asset prices '
                       'reduce wealth and shift AD left to AD2, moving it to E2 at lower output. '
                       'Arrows point both ways from AD0.'}},
    # id 319
    {'ch': 10,
     'q': 'A country enjoys an unexpected, one-time drop in the world price of the oil it imports. If '
          "households recognize that their higher income won't last, what does the AD–AS analysis "
          'predict about saving?',
     'opts': ['Saving rises, which can lower interest rates and add to capital formation',
              'Saving falls, as households dip into past savings to keep consumption up',
              'Saving rises, which raises interest rates and reduces capital formation',
              'Saving is unchanged, since a temporary shock leaves LRAS where it was'],
     'exp': 'People who know their extra income from a favorable supply shock is temporary save more '
            'of it. The added saving can lower interest rates and lead to additional capital '
            'formation.',
     'why': [None,
             'Dipping into past savings is the response to an **unfavorable** shock that temporarily '
             'lowers income, not to a favorable one.',
             'More saving adds to the supply of loanable funds, which lowers interest rates rather '
             'than raising them, and so encourages capital formation.',
             'An unchanged LRAS is exactly why households save more: they know the higher income will '
             'not last and set part of it aside.'],
     'fig': {'type': 'graph',
             'x': 'Real GDP',
             'y': 'Price level',
             'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD1'},
                       {'pts': [[20, 20], [85, 85]], 'cls': 's', 'label': 'SRAS1'},
                       {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
             'points': [{'at': [50, 50], 'label': 'E1'}],
             'guides': True,
             'xticks': [[50, 'YF']],
             'yticks': [[50, 'P1']],
             'alt': "The economy's starting position: a downward-sloping AD1 curve, an upward-sloping "
                    'SRAS1 curve, and a vertical LRAS line all pass through E1 at full-employment '
                    'output YF and price level P1. No curve has shifted yet.'},
     'expFig': {'type': 'graph',
                'x': 'Real GDP',
                'y': 'Price level',
                'lines': [{'pts': [[15, 85], [85, 15]], 'cls': 'd', 'label': 'AD1'},
                          {'pts': [[20, 20], [85, 85]], 'cls': 'm', 'label': 'SRAS1'},
                          {'pts': [[30, 10], [95, 75]], 'cls': 's', 'label': 'SRAS2', 'dash': True},
                          {'pts': [[50, 8], [50, 92]], 'cls': 'v', 'label': 'LRAS'}],
                'points': [{'at': [50, 50], 'label': 'E1'}, {'at': [60, 40], 'label': 'E2'}],
                'guides': True,
                'xticks': [[50, 'YF'], [60, 'Y2']],
                'yticks': [[40, 'P2'], [50, 'P1']],
                'arrows': [{'from': [62, 58], 'to': [76, 58]}],
                'alt': 'After the change: SRAS1 shifts right to SRAS2 while AD1 and LRAS stay put, '
                       'since the shock is temporary. AD1 crosses SRAS2 at E2, at output Y2 above YF '
                       'and the lower price level P2. An arrow points from SRAS1 toward SRAS2.'}},
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

# Retired questions stay in the list so question numbers never shift (weak spots are saved
# as numbers), but they are never asked.
ACTIVE = [i for i, q in enumerate(QUESTIONS) if not q.get("retired")]


def plain(text):
    """The web quiz marks key words as **bold**; the terminal just shows the words."""
    return text.replace("**", "")


def wrap(text, indent=""):
    return textwrap.fill(plain(text), WIDTH, initial_indent=indent, subsequent_indent=indent)


def show_figure(fig, indent="  "):
    """Print a table as aligned columns, or a graph as its written description."""
    if not fig:
        return
    if fig["type"] == "table":
        rows = [fig["head"]] + fig["rows"]
        widths = [max(len(str(r[c])) for r in rows) for c in range(len(fig["head"]))]
        for n, row in enumerate(rows):
            print(indent + "  ".join(str(cell).ljust(w) for cell, w in zip(row, widths)))
            if n == 0:
                print(indent + "  ".join("-" * w for w in widths))
    else:
        print(wrap("[Graph] " + fig["alt"], indent))


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
    letters = "1234"[:len(opts)]

    print("\n" + "-" * WIDTH)
    print(f"[{number}/{total}]  Ch. {item['ch']}: {CHAPTER_NAMES[item['ch']]}")
    print(wrap(item["q"]))
    show_figure(item.get("fig"))
    for letter, opt in zip(letters, opts):
        print(textwrap.fill(plain(opt), WIDTH, initial_indent=f"   {letter}) ", subsequent_indent="      "))

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
        show_figure(item.get("expFig"))
        return True
    print(f"  Not quite. Answer: {right_letter}) {plain(correct)}")
    print(wrap(item["exp"], "  "))
    show_figure(item.get("expFig"))
    why = item.get("why")
    if why:
        # why[k] explains wrong option k (in the original order); start with the one they picked
        picked = item["opts"].index(chosen)
        wrong = sorted((k for k in range(1, len(why)) if why[k]), key=lambda k: k != picked)
        print("  Why the other answers are wrong:")
        for k in wrong:
            mark = " (your answer)" if k == picked else ""
            print(wrap(f"- {plain(item['opts'][k])}{mark}: {why[k]}", "    "))
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
        count = sum(1 for i in ACTIVE if QUESTIONS[i]["ch"] == ch)
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
        missed = {i for i in load_missed() if i in ACTIVE}
        print("\nMenu:")
        print("  1) Practice all chapters")
        print("  2) Pick chapters")
        print(f"  3) Weak spots only ({len(missed)} saved)")
        print("  4) Clear weak spots")
        print("  5) Quit")
        choice = input("> ").strip()

        if choice == "1":
            run_round(ACTIVE[:])
        elif choice == "2":
            chs = choose_chapters()
            pool = [i for i in ACTIVE if QUESTIONS[i]["ch"] in chs]
            run_round(pool)
        elif choice == "3":
            pool = sorted(missed)
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
