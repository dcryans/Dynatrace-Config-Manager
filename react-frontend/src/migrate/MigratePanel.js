import * as React from 'react';
import EntityFilterSection from '../filter/EntityFilterSection';
import TenantMigrationSelector from '../credentials/TenantMigrationSelector';
import MigrateEntities from './MigrateEntities';
import ApplyMigrationBox from '../filter/ApplyMigrationBox';
import PreemptiveMigrationBox from '../filter/PreemptiveMigrationBox';

export default function MigratePanel() {

    return (
        <React.Fragment>
            <TenantMigrationSelector />
            <EntityFilterSection />
            <PreemptiveMigrationBox />
            <ApplyMigrationBox />
            <MigrateEntities />
        </React.Fragment>
    );
}
