# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Command.suggest_url'
        db.add_column('cli_command', 'suggest_url', self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'Command.suggest_url'
        db.delete_column('cli_command', 'suggest_url')
    
    
    models = {
        'cli.command': {
            'Meta': {'object_name': 'Command'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'last_used': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'suggest_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'use_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }
    
    complete_apps = ['cli']
