{{GOLANG_HEADER}}

package {{GOLANG_PACKAGE}}

import (
	"fmt"
	"time"

	"{{GOLANG_MODULE}}/internal/event"
)

var log = event.Logger()

type Types map[string]interface{}

// Entities List of database entities and their table names.
var Entities = Types{
	Password{}.TableName(): &Password{},
	User{}.TableName():     &User{},
	Example{}.TableName():  &Example{},
}

type RowCount struct {
	Count int
}

// WaitForMigration waits for the database migration to be successful.
func (list Types) WaitForMigration() {
	attempts := 100
	for name := range list {
		for i := 0; i <= attempts; i++ {
			count := RowCount{}
			if err := Db().Debug().Raw(fmt.Sprintf("SELECT COUNT(*) AS count FROM %s", name)).Scan(&count).Error; err == nil {
				// log.Printf("entity: table %s migrated", name)
				break
			} else {
				log.Printf("entity: wait for migration %s (%s)", err.Error(), name)
			}

			if i == attempts {
				panic("entity: migration failed")
			}

			time.Sleep(50 * time.Millisecond)
		}
	}
}

// Truncate removes all data from tables without dropping them.
func (list Types) Truncate() {
	for name := range list {
		if err := Db().Debug().Exec(fmt.Sprintf("DELETE FROM %s WHERE 1", name)).Error; err == nil {
			// log.Printf("entity: removed all data from %s", name)
			break
		} else if err.Error() != "record not found" {
			log.Printf("entity: %s in %s", err, name)
		}
	}
}

// Migrate migrates all database tables of registered entities.
func (list Types) Migrate() {
	for _, entity := range list {
		if err := UnscopedDb().Debug().AutoMigrate(entity); err != nil {
			log.Printf("entity: migrate %s (waiting 1s)", err.Error())

			time.Sleep(time.Second)

			if err = UnscopedDb().AutoMigrate(entity); err != nil {
				panic(err)
			}
		}
	}
}

// Drop drops all database tables of registered entities.
func (list Types) Drop() {
	for _, entity := range list {
		if err := UnscopedDb().Debug().Migrator().DropTable(entity).Error; err != nil {
			panic(err)
		}
	}
}

// MigrateDb creates all tables and inserts default entities as needed.
func MigrateDb() {
	Entities.Migrate()
	Entities.WaitForMigration()

	CreateDefaultFixtures()
}

// CreateDefaultFixtures inserts default fixtures for test and production.
func CreateDefaultFixtures() {
	CreateDefaultUsers()
}
