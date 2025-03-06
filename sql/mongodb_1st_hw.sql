    -- Из коллекции customers выяснить из какого города "Sven Ottlieb"
{
  filter: {
    ContactName: 'Sven Ottlieb'
  },
  project: {
    City: 1,
    _id: 0
  }
}
Result: Aachen

    -- Из коллекции ich.US_Adult_Income найти возраст самого взрослого человека
{
  sort: {
    age: -1
  },
  project: {
    age: 1,
    _id: 0
  }
}
Result: 90

    -- Из 2 задачи выясните, сколько человек имеют такой же возраст
{
  filter: {
    age: 90
  },
  sort: {
    age: -1
  },
  project: {
    age: 1,
    _id: 0
  }
}
Result: 43
    
    
    -- Найти _id ObjectId документа, в котором education " IT-career-hub"
{
  filter: {
    education: ' IT-career-hub'
  },
  project: {
    _id: 1
  }
}
Result: {
  "_id": {
    "$oid": "656e13232afc911a8a7ad5e5"
  }
}

    -- Выяснить количество людей в возрасте между 20 и 30 годами
    {
  filter: {
    age: {
      $gte: 20,
      $lt: 30
    }
  },
  project: {
    age: 1
  }
}
Result: 8915
