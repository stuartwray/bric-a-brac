// A small C++ program
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
#include <list>
#include <map>

#include <stdexcept>

#include <cstdlib>
#include <time.h>
#include <math.h>

// -----------------------------------------------------------------------
// helper routines

int RandN(int n)
{
  if (n <= 0 || n > RAND_MAX)
    throw std::domain_error("Argument to RandN is out of range");

  const int iBucketSize = RAND_MAX / n; // Note: rounds down
  int iResult = rand() / iBucketSize;

  while (iResult >= n)
  {
    // Must be in range [iBucketSize * n .. RAND_MAX]
    // Try again
    iResult = rand() / iBucketSize;
  }

  return iResult;
}

double log2(double x)
{
  return log(x) / log(2);
}

double Entropy(std::vector<int>& counts)
{
  // How many counts in total?
  int iTotal = 0;
  for (std::vector<int>::iterator i = counts.begin(); i != counts.end(); i++)
  {
    iTotal += *i;
  }

  // Cope with tricky case ...

  if (iTotal == 0)
    return 0.0;
              
  // Entropy, H = Sum (Pi * log2 (1/Pi))  

  double dEntropy = 0.0;
  for (std::vector<int>::iterator i = counts.begin(); i != counts.end(); i++)
  {
    if (*i == 0)
      continue;

    double dProb = ((double) *i) / iTotal;
    dEntropy += dProb * log2(1 / dProb);
  }
  
  return dEntropy;
}


// -----------------------------------------------------------------------

class Colour
{
private:
  std::string s;

public:
  Colour() { s = ""; }
  Colour(const char * psz_value) { s = psz_value;}

  bool operator== (const Colour& other) { return s == other.s; }
  bool operator!= (const Colour& other) { return s != other.s; }
  std::string Str() {return s;}
};

std::ostream& operator<<(std::ostream& os, Colour& c)
{
  os << c.Str();
  return os;
}
  
// -----------------------------------------------------------------------

class Position
{
private:
  static const int WIDTH = 4;
  std::vector<Colour> pegs;

public:

  Position()
    {
      pegs.resize(WIDTH);
      for (int i = 0; i < WIDTH; i++)
        pegs[i] = Colour();
    }

  Position(Colour& a, Colour& b, Colour& c, Colour& d) 
    { 
      pegs.resize(WIDTH);
      pegs[0] = a;
      pegs[1] = b;
      pegs[2] = c;
      pegs[3] = d;
    }

  Position(std::vector<Colour>& init) 
    { 
      pegs.resize(WIDTH);
      for (int i = 0; i < WIDTH; i++)
        pegs[i] = init[i];
    }

  bool operator== (const Position& other)
    {
      for (int i = 0; i < WIDTH; i++)
      {
        if (pegs[i] != other.pegs[i])
          return false;
      }
      return true;
    }

  bool operator!= (const Position& other)
    {
      for (int i = 0; i < WIDTH; i++)
      {
        if (pegs[i] != other.pegs[i])
          return true;
      }
      return false;
    }

  std::string Str() 
    {
      std::string result = pegs[0].Str(); // Assume at least one peg!
      for (int i = 1; i < WIDTH; i++) 
      {
        result += ".";
        result += pegs[i].Str();
      }

      return result; 
    }

  std::string Mark (Position& correct)
    {
      std::string result;

      bool done_this[WIDTH];
      bool done_correct[WIDTH];
      for (int i = 0; i < WIDTH; i++) 
      {
        done_this[i] = false;
        done_correct[i] = false;
      }

      // do black marks
      for (int i = 0; i < WIDTH; i++) 
      {
        if (pegs[i] == correct.pegs[i])
        {
          result += "b";
          done_this[i] = true;
          done_correct[i] = true;
        }
      }

      // do white marks
      for (int i = 0; i < WIDTH; i++) 
      {
        if (!done_this[i])
        {
          for (int j = 0; j < WIDTH; j++) 
          {
            if (!done_correct[j] &&
                pegs[i] == correct.pegs[j])
            {
              result += "w";
              done_this[i] = true;
              done_correct[j] = true;
              break;
            }
          }
        }
      }
      
      return result;
    }

  static Position MakeRandomPosition(std::vector<Colour>& colours)
    {
      int iHowManyColours = colours.size();
      std::vector<Colour> ours;

      for (int i = 0; i < WIDTH; i++)
      {
        ours.push_back(colours[RandN(iHowManyColours)]);
      }
      
      return Position(ours);
    }

  static std::list<Position> MakeAllPositions(std::vector<Colour>& colours)
    {
      int iHowManyColours = colours.size();
      std::list<Position> result;

      int iHowManyEntries = 1;
      for (int i = 0; i < WIDTH; i++)
        iHowManyEntries *= iHowManyColours;

      for (int i = 0; i < iHowManyEntries; i++)
      {
        int iCoded = i;

        std::vector<Colour> ours;
        for (int col = 0; col < WIDTH; col++)
        {
          int iColourIndex = iCoded % iHowManyColours;
          iCoded           = iCoded / iHowManyColours;
          ours.push_back(colours[iColourIndex]);
        }

        result.push_back(Position(ours));
      }

      return result;      
    }
};

std::ostream& operator<<(std::ostream& os, Position& p)
{
  os << p.Str();
  return os;
}
  
// -----------------------------------------------------------------------

int main()
{
  std::vector<Colour> all_colours;
  all_colours.push_back(Colour("red"));
  all_colours.push_back(Colour("green"));
  all_colours.push_back(Colour("blue"));
  all_colours.push_back(Colour("yellow"));
  all_colours.push_back(Colour("white"));
  all_colours.push_back(Colour("black"));
   
  // Initialise the random number generator with the time
  srand(time(NULL));

  // This is the secret position to guess
  Position secret = Position::MakeRandomPosition(all_colours);
  std::cout << "Secret is "  << secret <<  std::endl;

  // This is the list of challenges that we haven't used yet
  std::list<Position> challenges = Position::MakeAllPositions(all_colours);

  // This is the list of positions that are still plausible,
  // given the responses to challenges so far
  std::list<Position> candidates = Position::MakeAllPositions(all_colours);

  Position answer; // Where the answer will be put

  int attempt = 1;

  while (true)
  {
    std::cout << "(" << attempt++ << ") Candiates left = " << 
      candidates.size() << std::endl;
    Position guess; // Where this attempt's guess will be put

    if (candidates.size() == 1)
    {
      // We have notionally finished, but we still have to say what the
      // answer is
      guess = *(candidates.begin());
    }
    else
    {
      // Find the challenge with the highest entropy
      
      Position max_ent_pos;
      double max_ent = -1.0;
      
      // For all remaining challenges ...
      
      for (std::list<Position>::iterator challenge = challenges.begin();
           challenge != challenges.end();
           challenge++)
      {
        // Mark every remaining candidate
        
        std::map<std::string, int> mark2Count;
        for (std::list<Position>::iterator candidate = candidates.begin();
             candidate != candidates.end();
             candidate++)
        {
          std::string mark = candidate->Mark(*challenge);
          mark2Count[mark] += 1;
        }
        
        // Determine the entropy associated with this distribution of marks
        
        std::vector<int> markPartions;
        for (std::map<std::string, int>::const_iterator it = mark2Count.begin();
             it != mark2Count.end();
             it ++)
        {
          markPartions.push_back(it->second);
        }
        
        double entropy = Entropy(markPartions);
        
        // is this the best so far?
        
        if (entropy > max_ent)
        {
          max_ent_pos = *challenge;
          max_ent = entropy;
        }
      }  

      guess = max_ent_pos;
      std::cout << "    Max entropy " << max_ent <<  std::endl;
    }

    // Remove the challenge we just used
    remove(challenges.begin(), challenges.end(), guess);

    std::cout << "    Guess is "  << guess <<  std::endl;

    // ---------------------------------------------------
    // This part is notionally done by the other player

    std::string mark = secret.Mark(guess);
    std::cout << "Mark is \""  << mark <<  "\"" << std::endl;

    if (mark == "bbbb") // XXX Assumes width == 4 
    {
      answer = guess;
      break;
    }

    // Now back to the guesser
    // ---------------------------------------------------

    // Remove the candidates that are inconsistent with the answer we got

    std::list<Position>::iterator candidate = candidates.begin();
    while (candidate != candidates.end())
    {
      if (candidate->Mark(guess) == mark)
      {
        // This one is consistent so pass on to the next candidate
        candidate++;
      }
      else
      {
        // This one is not consistent, so remove it
        candidate = candidates.erase(candidate);
      }
    }
  }

  std::cout << "Solution is "  << answer <<  std::endl;
  std::cout << "------------------------------------------------------\n";

  return 0;
}

